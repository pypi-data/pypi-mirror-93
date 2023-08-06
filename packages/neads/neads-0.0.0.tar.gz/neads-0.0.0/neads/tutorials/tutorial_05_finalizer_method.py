import matplotlib.pyplot as plt


def tutorial_05_finalizer_method(data):
    values = [
        d['data']
        for _, d in
        sorted(data, key=lambda x: x[0].components[3].params['interval'])
    ]
    plt.plot(values)