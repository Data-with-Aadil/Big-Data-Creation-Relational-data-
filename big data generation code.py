import pandas as pd
import numpy as np
from faker import Faker
import random
import json

fake = Faker('en_IN')  # Use Indian locale

# Read support data with encoding
support_data = pd.read_csv('support_data.csv', encoding='latin-1')
indian_states_cities = pd.read_csv('indian_states_cities.csv', encoding='latin-1')

# Function to generate customer ID in specified format
# def generate_customer_id():
#     return f"CG-{fake.random_number(digits=5, fix_len=True)}"

def generate_customer_id(state):
    state_abbr = ''.join([word[0] for word in state.split() if word[0].isalpha()]).upper()
    return f"{state_abbr}-{fake.random_number(digits=5, fix_len=True)}"

# Function to generate transaction data
# def generate_transactions(num_transactions):
#     transactions = []
#     for _ in range(num_transactions):
#         customer_id = generate_customer_id()
#         product = support_data.sample(1).iloc[0]
#         product_id = product['product_id']
#         price = product['price']
#         quantity = random.randint(1, 5)
#         transaction_id = f"{customer_id}-{product_id}"
#         items = [{
#             'product_id': product_id,
#             'quantity': quantity,
#             'price': price
#         }]
#         transaction_date = fake.date_between(start_date='-3y', end_date='today')
#         transactions.append({
#             'transaction_id': transaction_id,
#             'customer_id': customer_id,
#             'date': transaction_date,
#             'items': json.dumps(items)
#         })
#     return pd.DataFrame(transactions)

# def generate_transactions(num_transactions):
#     transactions = []
#     for _ in range(num_transactions):
#         customer_id = generate_customer_id()
#         product = support_data.sample(1).iloc[0]
#         product_id = product['product_id']
#         price = product['price']
#         quantity = random.randint(1, 5)
#         transaction_id = f"{customer_id}-{product_id}-{fake.time(pattern='%M%S')}"
#         items = [{
#             'product_id': product_id,
#             'quantity': quantity,
#             'price': price
#         }]
#         transaction_date = fake.date_between(start_date='-3y', end_date='today')
#         transactions.append({
#             'transaction_id': transaction_id,
#             'customer_id': customer_id,
#             'date': transaction_date,
#             'items': json.dumps(items)
#         })
#     return pd.DataFrame(transactions)

def generate_transactions(num_transactions):
    transactions = []
    customers_with_multiple_transactions = set()

    # Ensure 37% of customers have multiple transactions
    num_customers = int(num_transactions * 0.37)
    for _ in range(num_customers):
        state = indian_states_cities.sample(1)['State'].values[0]
        customer_id = generate_customer_id(state)
        customers_with_multiple_transactions.add(customer_id)
        num_customer_transactions = random.randint(2, 5)  # Each customer can have between 2 and 5 transactions
        for _ in range(num_customer_transactions):
            product = support_data.sample(1).iloc[0]
            product_id = product['product_id']
            price = f"${product['price']}"
            quantity = random.randint(1, 5)
            transaction_id = f"{customer_id}-{product_id}-{fake.time(pattern='%M%S')}"
            items = [{
                'product_id': product_id,
                'quantity': quantity,
                'price': price
            }]
            transaction_date = fake.date_between(start_date='-3y', end_date='today')
            transactions.append({
                'transaction_id': transaction_id,
                'customer_id': customer_id,
                'date': transaction_date,
                'items': json.dumps(items)
            })

    # Remaining transactions to ensure we reach the total number desired
    remaining_transactions = num_transactions - len(transactions)
    for _ in range(remaining_transactions):
        customer_id = generate_customer_id()
        product = support_data.sample(1).iloc[0]
        product_id = product['product_id']
        price = f"${product['price']}"
        quantity = random.randint(1, 5)
        transaction_id = f"{customer_id}-{product_id}-{fake.time(pattern='%M%S')}"
        items = [{
            'product_id': product_id,
            'quantity': quantity,
            'price': price
        }]
        transaction_date = fake.date_between(start_date='-3y', end_date='today')
        transactions.append({
            'transaction_id': transaction_id,
            'customer_id': customer_id,
            'date': transaction_date,
            'items': json.dumps(items)
        })

    return pd.DataFrame(transactions)



# Generate Transactions data
num_transactions = 150000  # Example size
transactions = generate_transactions(num_transactions)
transactions.to_csv('transactions.csv', index=False)

# Function to generate unique customer data
# def generate_customers(transaction_data):
#     customers = []
#     unique_customers = transaction_data['customer_id'].unique()
#     for customer_id in unique_customers:
#         customer_transactions = transaction_data[transaction_data['customer_id'] == customer_id]
#         purchase_history = customer_transactions['transaction_id'].tolist()
#         customers.append({
#             'customer_id': customer_id,
#             'name': fake.unique.name(),
#             'membership_level': random.choice(['Silver', 'Gold', 'Platinum']),
#             'geographic_region': indian_states_cities.sample(1)['State'].values[0],  # Indian states
#             'purchase_history': json.dumps(purchase_history)  # Convert the list to a JSON string
#         })
#     return pd.DataFrame(customers)

# customers = generate_customers(transactions)
# customers.to_csv('customers.csv', index=False)

def generate_customers(transaction_data):
    customers = []
    unique_customers = transaction_data['customer_id'].unique()
    for customer_id in unique_customers:
        state = indian_states_cities.sample(1)['State'].values[0]
        purchase_history = []
        for _, row in transaction_data[transaction_data['customer_id'] == customer_id].iterrows():
            purchase_history.append(row['transaction_id'])

        purchase_history = json.dumps(purchase_history)

        customers.append({
            'customer_id': customer_id,
            'name': fake.name(),
            'membership_level': random.choice(['Silver', 'Gold', 'Platinum']),
            'geographic_region': state,
            'purchase_history': purchase_history
        })
    return pd.DataFrame(customers)

customers = generate_customers(transactions)
customers.to_csv('customers.csv', index=False)

# Function to generate unique product data
# def generate_products(transaction_data):
#     product_ids = []
#     for _, row in transaction_data.iterrows():
#         items = json.loads(row['items'])
#         for item in items:
#             product_ids.append(item['product_id'])

#     product_ids = list(set(product_ids))  # Remove duplicates

#     products = support_data[support_data['product_id'].isin(product_ids)].copy()
#     products['attributes'] = products.apply(lambda row: json.dumps({
#         'product_category': row['category'],
#         'sub_category': row['sub_category']
#     }), axis=1)
#     return products[['product_id', 'product_name', 'attributes', 'price']]

def generate_products(transaction_data):
    product_ids = []
    for _, row in transaction_data.iterrows():
        items = json.loads(row['items'])
        for item in items:
            product_ids.append(item['product_id'])

    product_ids = list(set(product_ids))  # Remove duplicates

    products = support_data[support_data['product_id'].isin(product_ids)].copy()
    products['attributes'] = products.apply(lambda row: json.dumps({
        'product_category': row['category'],
        'sub_category': row['sub_category']
    }), axis=1)
    products['price'] = products['price'].apply(lambda x: f"${x}")
    products.rename(columns={'product_name': 'description'}, inplace=True)
    return products[['product_id', 'description', 'attributes', 'price']]


products = generate_products(transactions)
products.to_csv('products.csv', index=False)

# Adjusted promotional occasions with Indian festivals
occasion_promotions = {
    "Diwali Sale": {"start": "10-15", "end": "11-15"},
    "Holi Special": {"start": "03-10", "end": "03-20"},
    "Eid Discount": {"start": "05-20", "end": "06-20"},
    "Christmas Offer": {"start": "12-15", "end": "12-25"},
    "Independence Day Sale": {"start": "08-10", "end": "08-20"},
    "Republic Day Special": {"start": "01-20", "end": "01-30"},
    "Ganesh Chaturthi Sale": {"start": "09-05", "end": "09-15"},
    "Navratri Discount": {"start": "09-20", "end": "10-10"},
    "Raksha Bandhan Offer": {"start": "08-01", "end": "08-10"},
    "New Year Sale": {"start": "01-01", "end": "01-10"},
}

# Generate promotions with correct date formatting and discount range
def generate_promotions(products):
    promotions = []
    for promo, dates in occasion_promotions.items():
        applicable_products = random.sample(list(products['product_id']), random.randint(1, 10))
        start_date = dates['start']
        end_date = dates['end']
        promotions.append({
            'promo_id': fake.unique.uuid4(),
            'description': promo,
            'discount': round(random.uniform(5.0, 20.0), 2),
            'applicable_products': json.dumps(applicable_products),  # Store as JSON string
            'start_date': start_date.split('-')[1],
            'start_date_month': start_date.split('-')[0],
            'end_date': end_date.split('-')[1],
            'end_date_month': end_date.split('-')[0]
        })
    return pd.DataFrame(promotions)

promotions = generate_promotions(products)
promotions.to_csv('promotions.csv', index=False)

# Generate Refunds data
# def generate_refunds(num_refunds, transactions):
#     refunds = []
#     for _ in range(num_refunds):
#         transaction = transactions.sample(1).iloc[0]
#         items = json.loads(transaction['items'])
#         product = random.choice(items)
#         refund_quantity = random.randint(1, product['quantity'])
#         refund_amount = refund_quantity * product['price']
#         tax_rate = 0.1  # Example tax rate, adjust as needed
#         tax_refund_amount = refund_amount * tax_rate

#         refunds.append({
#             'refund_id': f"{transaction['customer_id']}-{transaction['transaction_id']}",
#             'transaction_id': transaction['transaction_id'],
#             'customer_id': transaction['customer_id'],
#             'product_id': product['product_id'],
#             'date': fake.date_between(start_date=transaction['date'], end_date=transaction['date'] + pd.Timedelta(days=15)),
#             'quantity': refund_quantity,
#             'refund_amount': round(refund_amount, 2),
#             'tax_refund_amount': round(tax_refund_amount, 2)
#         })
#     return pd.DataFrame(refunds)

# num_refunds = 17000  # Example size
# refunds = generate_refunds(num_refunds, transactions)
# refunds.to_csv('refunds.csv', index=False)

def generate_refunds(num_refunds, transactions):
    refunds = []
    for _ in range(num_refunds):
        transaction = transactions.sample(1).iloc[0]
        items = json.loads(transaction['items'])
        product = random.choice(items)
        refund_quantity = random.randint(1, product['quantity'])
        refund_amount = refund_quantity * float(product['price'].replace('$', ''))  # Convert to float and remove '$'
        tax_rate = 0.1  # Example tax rate, adjust as needed
        tax_refund_amount = refund_amount * tax_rate

        refunds.append({
            'refund_id': f"{transaction['customer_id']}-{transaction['transaction_id']}",
            'transaction_id': transaction['transaction_id'],
            'customer_id': transaction['customer_id'],
            'product_id': product['product_id'],
            'date': fake.date_between(start_date=transaction['date'], end_date=transaction['date'] + pd.Timedelta(days=15)),
            'quantity': refund_quantity,
            'refund_amount': f"${round(refund_amount, 2)}",  # Add '$' back after multiplication
            'tax_refund_amount': f"${round(tax_refund_amount, 2)}"  # Add '$' back after multiplication
        })
    return pd.DataFrame(refunds)

num_refunds = 17000  # Example size
refunds = generate_refunds(num_refunds, transactions)
refunds.to_csv('refunds.csv', index=False)
