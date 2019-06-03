import requests

url = 'http://127.0.0.1:5000'   # The root url of the flask app


def test_create():
    r = requests.post(
        url+'/purses',
        json={"ccy": "UAH", "total": 50})
    obj = r.json()
    assert obj.get("id") is not None
    assert r.status_code == 200


def test_get_by_id():
    r = requests.post(
        url + '/purses',
        json={"ccy": "UAH", "total": 50}
     )
    obj = r.json()
    purse_id = str(obj.get("id"))
    res = requests.get(url + '/purses/' + purse_id)
    o = res.json()
    assert o.get("ccy") == "UAH"
    assert o.get("total") == 50
    assert res.status_code == 200
    requests.delete(url + '/purses/' + purse_id)


def test_delete():
    r = requests.post(
        url + '/purses',
        json={"ccy": "UAH", "total": 50})
    obj = r.json()
    purse_id = str(obj.get("id"))
    res = requests.delete(url + '/purses/' + purse_id)
    assert res.status_code == 200


def test_upd():
    r = requests.post(
        url + '/purses',
        json={"ccy": "UAH", "total": 50})
    obj = r.json()
    purse_id = str(obj.get("id"))
    res = requests.put(
        url + '/purses/' + purse_id,
        json={ "ccy": "EUR", "total": 85})
    assert res.status_code == 200
    res = requests.get(url + '/purses/' + purse_id)
    o = res.json()
    assert o.get("ccy") == "EUR"
    assert o.get("total") == '85'
