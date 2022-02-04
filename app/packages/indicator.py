import typing
import pandas as pd

class Indicator:

    def get_bollinger_bands(self, prices, intervals):
        prices = pd.Series(prices)
        sma = prices.rolling(intervals).mean()
        std = prices.rolling(intervals).std()
        bollinger_up = sma + std * 2
        bollinger_down = sma - std * 2
        sma = sma.tolist()
        std = std.tolist()
        bollinger_up = bollinger_up.tolist()
        bollinger_down = bollinger_down.tolist()
        return sma, bollinger_up, bollinger_down

    def get_sma(self, prices, intervals):
        prices = pd.Series(prices)
        sma = prices.rolling(window=intervals).mean()
        sma = sma.tolist()
        return sma

    def get_macd(self, price, slow, fast, smooth):
        price = pd.DataFrame({'close': price})
        fastEma = price.ewm(span = fast, adjust = False).mean()
        slowEma = price.ewm(span = slow, adjust = False).mean()
        macd = pd.DataFrame(fastEma - slowEma).rename(columns = {'close':'macd'})
        signal = pd.DataFrame(macd.ewm(span = smooth, adjust = False).mean()).rename(columns = {'macd':'signal'})
        hist = pd.DataFrame(macd['macd'] - signal['signal']).rename(columns = {0:'hist'})
        return [macd['macd'].iloc[-1], signal['signal'].iloc[-1], hist['hist'].iloc[-1]]

    def get_rsi(self, data: typing.List[float or int], window_length: int,
                    use_rounding: bool = True) -> typing.List[typing.Any]:
        do_round = lambda x: round(x, 2) if use_rounding else x  # noqa: E731
        gains: typing.List[float] = []
        losses: typing.List[float] = []
        prev_avg_gain: float or None = None
        prev_avg_loss: float or None = None
        for i, price in enumerate(data):
            if i == 0:
                continue
            difference = do_round(data[i] - data[i - 1])
            if difference > 0:
                gain = difference
                loss = 0
            elif difference < 0:
                gain = 0
                loss = abs(difference)
            else:
                gain = 0
                loss = 0
            gains.append(gain)
            losses.append(loss)
            if i < window_length:
                continue
            if i == window_length:
                avg_gain = sum(gains) / len(gains)
                avg_loss = sum(losses) / len(losses)
            else:
                avg_gain = (prev_avg_gain * (window_length - 1) + gain) / window_length
                avg_loss = (prev_avg_loss * (window_length - 1) + loss) / window_length
            avg_gain = do_round(avg_gain)
            avg_loss = do_round(avg_loss)
            prev_avg_gain = avg_gain
            prev_avg_loss = avg_loss
            rs = do_round(avg_gain / avg_loss)
            rsi = do_round(100 - (100 / (1 + rs)))
            gains.pop(0)
            losses.pop(0)
        return rsi