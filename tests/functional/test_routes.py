from iebank_api import app, db
from iebank_api.models import Accounts
import pytest

def test_get_accounts(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/accounts')
    assert response.status_code == 200

def test_dummy_wrong_path():
    """
    GIVEN a Flask application
    WHEN the '/wrong_path' page is requested (GET)
    THEN check the response is valid
    """
    with app.test_client() as client:
        response = client.get('/wrong_path')
        assert response.status_code == 404

def test_create_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is posted to (POST)
    THEN check the response is valid
    """
    testing_client.post('/accounts', json={'name': 'John Doe', 'currency': '€', 'country': 'Spain'})
    response_1 = testing_client.get('/accounts')
    assert response_1.status_code == 200
    


def test_get_accounts_1(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is requested (GET)
    THEN check that a valid response is returned and the data is correct
    """
    # Create some accounts to fetch
    testing_client.post('/accounts', json={'name': 'John Doe', 'currency': '€', 'country': 'Spain'})
    testing_client.post('/accounts', json={'name': 'John Dee', 'currency': '€', 'country': 'Spain'})
    
    # Retrieve all accounts
    response = testing_client.get('/accounts')
    assert response.status_code == 200
    data = response.get_json()
    
    assert len(data['accounts']) >= 2  # Check if at least 2 accounts exist
    assert data['accounts'][1]['name'] == 'John Doe'
    assert data['accounts'][2]['name'] == 'John Dee'



def test_get_specific_account(testing_client):
    """
    GIVEN a Flask application
    WHEN a GET request is made to '/accounts/<id>'
    THEN check that the correct account is returned
    """
    # Create an account to retrieve
    response = testing_client.post('/accounts', json={
        'name': 'Charlie',
        'currency': '£',
        'country': 'UK'
    })
    account_id = response.get_json()['id']
    
    # Retrieve the specific account
    response = testing_client.get(f'/accounts/{account_id}')
    assert response.status_code == 200
    data = response.get_json()
    
    assert data['name'] == 'Charlie'
    assert data['currency'] == '£'
    assert data['country'] == 'UK'

def test_update_account(testing_client):
    """
    GIVEN a Flask application
    WHEN a PUT request is made to '/accounts/<id>'
    THEN check that the account is updated correctly
    """
    # Create an account to update
    response = testing_client.post('/accounts', json={
        'name': 'Alice',
        'currency': '$',
        'country': 'USA'
    })
    account_id = response.get_json()['id']

    # Update the account
    response = testing_client.put(f'/accounts/{account_id}', json={
        'name': 'Alice Updated',
    })
    
    assert response.status_code == 200
    updated_data = response.get_json()  # Check if the response includes updated data
    
    # Verify the account was updated
    assert updated_data['name'] == 'Alice Updated'


def test_delete_account(testing_client):
    """
    GIVEN a Flask application
    WHEN a DELETE request is made to '/accounts/<id>'
    THEN check that the account is deleted successfully
    """
    # Create an account to delete
    response = testing_client.post('/accounts', json={
        'name': 'David',
        'currency': '€',
        'country': 'Italy'
    })
    account_id = response.get_json()['id']
    
    # Delete the account
    response = testing_client.delete(f'/accounts/{account_id}')
    assert response.status_code == 200



def test_delete_nonexistent_account(testing_client):
    """
    GIVEN a Flask application
    WHEN a DELETE request is made to '/accounts/<id>' for a nonexistent account
    THEN check that a 404 status code is returned
    """
    nonexistent_id = 999999  # Arbitrary non-existing ID
    response = testing_client.delete('/accounts/{nonexistent_id}')
    assert response.status_code == 404
