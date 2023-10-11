from ewm import AverageEWM, VarianceEWM, SampleSharpeEWM

if __name__ == "__main__":
    values = [0.1, 0.4, -0.2, 0.3, 0.1]
    aves = AverageEWM(0.1).ewm(values)
    vars = VarianceEWM(0.3).ewm(values)
    sharpes = SampleSharpeEWM(0.01).ewm(values)
    print(aves)
    print(vars)
    print(sharpes)
