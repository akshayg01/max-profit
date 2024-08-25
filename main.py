import pandas as pd

def maxProfitWithTransactions(prices):
    n = len(prices)
    if n == 0:
        return 0, []
    
    maxTransactions = 5
    dp = [[0] * (maxTransactions + 1) for _ in range(n)]
    buySell = [[[] for _ in range(maxTransactions + 1)] for _ in range(n)]
    
    for j in range(1, maxTransactions + 1):
        maxDiff = -prices[0]
        prevBuyDay = 0
        
        for i in range(1, n):
            if prices[i] + maxDiff > dp[i-1][j]:
                dp[i][j] = prices[i] + maxDiff
                buySell[i][j] = buySell[prevBuyDay][j-1] + [(prevBuyDay, i)]
            else:
                dp[i][j] = dp[i-1][j]
                buySell[i][j] = buySell[i-1][j]
            
            if dp[i][j-1] - prices[i] > maxDiff:
                maxDiff = dp[i][j-1] - prices[i]
                prevBuyDay = i
    
    return dp[n-1][maxTransactions], buySell[n-1][maxTransactions]

def addPurchaseSellColumns(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Ensure the data is sorted by date (if there's a date column)
    df = df.sort_values('date')

    # Extract the 'close' prices for computation
    prices = df['close'].tolist()

    # Calculate the maximum profit and the transactions
    _, transactions = maxProfitWithTransactions(prices)

    # Initialize 'purchase' and 'sell' columns
    df['purchase'] = 'No'
    df['sell'] = 'No'

    # Mark the purchase and sell days
    for buy, sell in transactions:
        df.at[buy, 'purchase'] = 'Yes'
        df.at[sell, 'sell'] = 'Yes'

    # Save the updated DataFrame to a new CSV file
    output_csv = csv_file.replace('.csv', '_with_transactions.csv')
    df.to_csv(output_csv, index=False)

    return output_csv

# Example usage
csv_file = 'stock_prices.csv'  # Replace with your CSV file path
output_file = addPurchaseSellColumns(csv_file)
print(f"Updated CSV file with transactions: {output_file}")
