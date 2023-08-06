"""Module providing class that evaluates a computation graph."""

# TODO: consider splitting the long methods

from __future__ import annotations

from typing import TYPE_CHECKING, Iterable
from collections import deque
from abc import ABC, abstractmethod
from pathlib import Path

from neads.executable_node_factory import ExecutableNodeFactory
from neads.memory_manager import MemoryManager
from neads.computation_graph import ComputationGraph
import neads.logger as logger

if TYPE_CHECKING:
    from neads.database import Database
    from neads.plugin_pool import PluginPool
    from neads.executable_nodes import ExecutableNode
    from neads.configuration import Configuration


class ComputationManager(ABC):
    """Common base class for of Computation managers."""

    def __init__(self, database: Database, plugin_pool: PluginPool,
                 tmp_dir: Path):
        """Initialize a ComputationManager instance.

        Parameters
        ----------
        database : Database
            Database from which the computation manager may load data
            and where it will store them.
        plugin_pool
            PluginPool from which will be loaded the plugins.
        tmp_dir
            Directory for storing temporary files by MemoryManager.
        """

        self.database = database
        self.plugin_pool = plugin_pool
        self.tmp_dir = tmp_dir

    @abstractmethod
    def compute(self, configuration: Configuration):
        """Computes the given configuration.

        Parameters
        ----------
        configuration
            Description of the desired computation.
        """

        pass


class SingleThreadedComputationManager(ComputationManager):
    """Computation manager which uses only one thread for evaluation."""

    def compute(self, configuration: Configuration):
        """Computes the given configuration.

        Parameters
        ----------
        configuration
            Description of the desired computation.
        """

        memory_manager = MemoryManager(self.tmp_dir)
        executable_nodes_factory = ExecutableNodeFactory(
            memory_manager.issue_data_instance
        )
        graph = ComputationGraph(configuration,
                                 executable_nodes_factory)
        # Note: plugin_pool may be there as an argument
        if graph.is_evolving:
            logger.info('Start evaluation of evolvers', 1)
            evolvers = graph.get_evolvers()
            self._eval_targets(evolvers)
            logger.info('End evaluation of evolvers', -1)
        logger.info('Start evaluation of finalizers', 1)
        finalizers = graph.get_finalizers()
        self._eval_targets(finalizers)
        logger.info('End evaluation of finalizers', -1)

    def _eval_targets(self, targets: Iterable[ExecutableNode]):
        """Evaluate the given targets and dependent nodes, if needed.

        The focus is on evaluation of targets.

        For example, if the data of targets are found in the database,
        no other nodes are evaluated. On the other hand, if they are not
        found, their parents must be evaluated and than comes time to
        the targets.

        Parameters
        ----------
        targets
            Collection of nodes to be evaluated.
        """

        nodes_to_execute = self._do_loading_step(targets)
        self._do_execution(nodes_to_execute)

    def _do_loading_step(self, targets: Iterable[ExecutableNode]):
        """Try to load the targets or their closest ancestors.

        Parameters
        ----------
        targets
            Collection of nodes which will be tried to load first.

        Returns
        -------
        Iterable[ExecutableNode]
            Collection of nodes that were not loaded successfully.
        """

        def append_non_included_parents(parents):
            for parent in parents:
                if parent not in attempted_to_load:
                    attempted_to_load.add(parent)
                    nodes_to_load.append(parent)

        logger.info('Start loading step', 1)
        nodes_to_load = deque(targets)
        attempted_to_load = set(targets)
        nodes_to_execute = []
        while nodes_to_load:
            node = nodes_to_load.popleft()
            logger.info(f'Try load {node}', 1)
            if not node.try_load(self.database):
                logger.info('FAIL', 0)
                nodes_to_execute.append(node)
                append_non_included_parents(node.parents)
            else:
                logger.info('SUCCESS', 0)
            logger.change_indent(-1)  # to have F/S indented
        logger.info('End loading step', -1)
        return nodes_to_execute

    def _do_execution(self, nodes_to_execute: Iterable[ExecutableNode]):
        """Execute the given nodes.

        Parameters
        ----------
        nodes_to_execute
            Collection of nodes to be executed.
        """

        logger.info('Start execution step', 1)
        nodes_to_execute = sorted(nodes_to_execute,
                                  key=lambda n: n.get_depth(),
                                  reverse=True)
        # nodes need to be evaluated one by one, starting with the ones
        # with the least depth
        # nodes are popped, ie. taken from the last index, thus the reverse
        while nodes_to_execute:
            node = nodes_to_execute.pop()
            logger.info(f'Execute {node}', 1)
            node.execute(self.database, self.plugin_pool)
            logger.change_indent(-1)
        logger.info('End execution step', -1)
