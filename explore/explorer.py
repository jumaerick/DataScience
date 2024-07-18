from commonLibraries.libraries import *
from loadData import dataLoader

dataset = dataLoader.readFile()


def getSummaries():
    st.table(dataset.describe())


def checkNormalDist():
    st.text("Check if the features follow normal distribution")
    sns.pairplot(dataset, diag_kind='kde')
    st.pyplot(plt)
    st.markdown("""
    - The wide top for revenue curve imply wide variations in the datasets. This explains the large standard deviations 
                for revenue in the data summaries.
    - The curves for the costs imply possibility of two classes.
    - The curves for the conversion_rate imply possibility of three  overlapping classes.
    """)


def scatterPlots(feature_x, feature_y, hue=None):
    col1, col2, col3 = st.columns(3)
    with col1:

        feature_x = st.selectbox(
            'Feature X', ('Cost', 'Revenue', 'Conversion_Rate'))

    with col3:

        feature_y = st.selectbox(
            'Feature y', ('Revenue', 'Cost', 'Conversion_Rate'))

    feature_x = feature_x.lower()
    feature_y = feature_y.lower()

    st.markdown(f"A plot of variation of {feature_x} and {feature_y}")
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=feature_x, y=feature_y, hue=hue, data=dataset)
    st.pyplot(plt)
    st.markdown("""
    - Paid advertising is the most expensive channel and email marketing is the cheapest channel in terms of cost.
    """)


def groupedData():
    customers_copy = dataset.copy()
    metric = st.selectbox('Select metric', ('Average', 'Total'))
    x = 'average'
    y = 'total'
    if metric == 'Average':
        grouped_data = customers_copy.groupby('channel', as_index=False)[
            ['revenue', 'cost', 'conversion_rate']].mean()
        x = y = 'average'
    else:
        grouped_data = customers_copy.groupby('channel', as_index=False)[
            ['revenue', 'cost', 'conversion_rate']].sum()
        x = y = 'total'
    # st.dataframe(grouped_data)

    # metric = metrice.lower()

    st.markdown(f'A scatterplot of {x} cost and {y} revenue')

    plt.figure(figsize=(9, 6))
#         sns.
    sns.scatterplot(x='cost', y='revenue',
                    data=grouped_data,
                    c=[color for color in range(len(grouped_data))],
                    s=100)
    plt.xlabel(f'{x} Cost')
    plt.ylabel(f'{y} Revenue')
    for i in range(len(grouped_data)):
        #     print(rev_cost.channel[i])
        plt.text(grouped_data['cost'][i], grouped_data['revenue'][i], f'%s,\n %i, %f' % (
            grouped_data['channel'][i], grouped_data['cost'][i], grouped_data['revenue'][i]))
    st.pyplot(plt)

    if metric == 'mean':
        st.markdown("""
        - Paid advertising is the most expensive channel and email marketing is the cheapest in terms of average costs.
        - Customers acquired from paid advertising are the most expensive in terms of acquisition costs, so the company should try as much as possible to retain them.
        - Customers from email campaign are valuable with the average revenue almost the same as that for paid advertising despite their 
                    lower average aquisition costs.
        - Customers from social media have the lowest average revenue.

        """)
    else:
        st.markdown("""
        - Email marketing is the most valuable channel generating the highest total revenue followed by referral channel.
        - Paid advertising despite being expensive generated lower revenue only above social media.
        - Customers from social media generated the lowest total revenue.

        """)
        pass


def conversionbyChannel():
    st.subheader('Average conversion rate by channel')
    def x(x): return x.round(2)
    customers_copy = dataset.copy()
    customers_copy['conversion_rate'] = x(
        customers_copy['conversion_rate'].values*100)
    avg_conversion = customers_copy.groupby('channel', as_index=False)['conversion_rate'].mean().sort_values(
        by='conversion_rate',
        ascending=False
    )
    avg_conversion['conversion_rate'] = x(avg_conversion['conversion_rate'])
    fig, ax = plt.subplots(figsize=(10, 6))
    ax = sns.barplot(y="%s" % ('channel'), x='conversion_rate',
                     data=avg_conversion, hue='channel')
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f%%')
    plt.xlabel('Average Conversion Rate')
    # plt.text(10, 5, 5)

    st.pyplot(plt)
    st.markdown("""
    - Social media is the best converting channel followed by referral. It is worth noting that both of these channels have a low average cost and high average revenue.
    - Paid advertising is the lowest converting channel despite it being the most expensive.
    - Email marketing although being the cheapest, it has a low conversion rate.
    """)


def roiCalculator():
    st.markdown("ROI of a channel refers to average revenue over average cost")
    grouped_data = dataset.groupby('channel', as_index=False)[
        ['revenue', 'cost']].mean().sort_values(by='cost')
    grouped_data['roi'] = grouped_data['revenue'] / grouped_data['cost']
    fig, ax = plt.subplots(figsize=(10, 6))
    ax = sns.barplot(x='channel', y='roi', data=grouped_data, hue='channel')
    st.pyplot(plt)
    st.markdown("""
    - Email marketing has the highest return on investment and paid advertising channel has the lowest.
    """)


def cltvCalcultor():
    """
    This function will complute the customer life time value using the formula
    """
    # CLTV = (revenue - cost) * conversion_rate / cost
    customers_copy = dataset.copy()
    customers_copy['cltv'] = (customers_copy['revenue'] - customers_copy['cost']) * customers_copy[
        'conversion_rate'] / customers_copy['cost']

    grouped_cltv = customers_copy.groupby('channel', as_index=False)[
        'cltv'].mean().sort_values(by='cltv', ascending=False)
    box_topcltvs = customers_copy.loc[customers_copy['channel'].isin(
        ['social media', 'referral'])]
    plt.figure(figsize=(8, 6))
    sns.barplot(x='channel', y='cltv', data=grouped_cltv, hue='channel')
    plt.title("The average CLTV of each channel")
    st.pyplot(plt)
    plt.figure(figsize=(8, 6))
    plt.title("The two channels with high average CLTV")
    sns.boxplot(x='channel', y='cltv', data=box_topcltvs, hue='channel')
    plt.legend(box_topcltvs['channel'].unique(), loc='best')
    st.pyplot(plt)
