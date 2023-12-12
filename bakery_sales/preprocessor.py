import pandas as pd

def preprocess(df):
    df['date_time'] = df['date'] + ' ' + df['time']
    df['date_time'] = pd.to_datetime(df['date_time'])

    # Extract the articles and the quantities in order to transform them into column s through a pivot method.
    # We'll now have 149 column, one per product with the corresponding qty
    pivot = df[['article', 'Quantity']]
    products = pivot.pivot(columns = 'article', values = 'Quantity')

    # Merge the pivot table with the original dataset and fill the Nan with zeros
    # Now for each date point we have the quantity of the article sold
    data = df.merge(products, left_index = True, right_index = True)
    data = data.fillna(value = 0)

    # Keep only the top 7 products (representing 68% of the volume sold)
    # Set date as index
    data_target = data[['date_time', 'TRADITIONAL BAGUETTE', 'CROISSANT', 'COUPE', 'PAIN AU CHOCOLAT', 'BAGUETTE', 'BANETTE', 'CEREAL BAGUETTE']]
    data_target = data_target.resample('60min', on = 'date_time').sum()

    data_target = data_target.rename(columns = {'TRADITIONAL BAGUETTE' : 'traditional_baguette',
                                                'CROISSANT' : 'croissant',
                                                'COUPE' : 'coupe',
                                                'PAIN AU CHOCOLAT' : 'pain_au_chocolat',
                                                'BAGUETTE' : 'baguette',
                                                'BANETTE' : 'banette',
                                                'CEREAL BAGUETTE' : 'cereal_baguette'})


    # Removing the empty rows
    data_target = data_target[data_target != 0]
    data_target.dropna(axis = 0, how = 'all', inplace = True)
    data_target = data_target.fillna(value = 0)


    return(data_target)