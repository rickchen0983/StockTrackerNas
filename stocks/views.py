from django.shortcuts import render
from django.http import JsonResponse
import yfinance as yf
import pandas as pd

# 安全轉 list 的 helper function
def safe_tolist(data):
    if isinstance(data, pd.Series):
        return data.tolist()
    elif isinstance(data, pd.DataFrame):
        return data.squeeze().tolist()  # 如果是 DataFrame（單欄），轉 Series 再 list
    return []

# 顯示首頁
def home(request):
    return render(request, 'StockTrackerMain.html')

# 抓取股票資料
def get_stock_data(request):
    stock_symbol = request.GET.get('symbol', '').upper()
    interval = request.GET.get('interval', '1d')

    if not stock_symbol:
        return JsonResponse({'error': '請輸入股票代碼'}, status=400)

    try:
        # 設定資料期間
        if interval == '1d':
            period = '3mo'  # 默認拉取三個月的資料
        elif interval == '1wk':
            period = '6mo'
        elif interval == '1mo':
            period = '2y'
        else:
            return JsonResponse({'error': '無效的 interval'}, status=400)

        # 抓取資料
        data = yf.download(stock_symbol, period=period, interval=interval)

        if data.empty:
            raise ValueError("無法取得資料，請確認股票代碼是否正確")

        # 當資料不足時，拉取更多資料
        if len(data) < 60:
            data = yf.download(stock_symbol, period='6mo', interval=interval)

        # 刪除包含 NaN 的行
        data.dropna(inplace=True)

        # 計算移動平均
        data['MA5'] = data['Close'].rolling(window=5).mean()
        data['MA20'] = data['Close'].rolling(window=20).mean()
        data['MA60'] = data['Close'].rolling(window=60).mean()

        # 填補 MA5, MA20, MA60 中的 NaN 值
        data['MA5'] = data['MA5'].fillna(method='bfill')
        data['MA20'] = data['MA20'].fillna(method='bfill')
        data['MA60'] = data['MA60'].fillna(method='bfill')  # 填補 NaN 值

        # 準備回傳資料
        response = {
            'dates': data.index.strftime('%Y-%m-%d').tolist(),
            'open': safe_tolist(data['Open']),
            'high': safe_tolist(data['High']),
            'low': safe_tolist(data['Low']),
            'close': safe_tolist(data['Close']),
            'volume': safe_tolist(data['Volume']),
            'ma5': safe_tolist(data['MA5']),
            'ma20': safe_tolist(data['MA20']),
            'ma60': safe_tolist(data['MA60']),
        }

        return JsonResponse(response)

    except Exception as e:
        return JsonResponse({'error': f"無法取得股票資料：{str(e)}"}, status=400)
