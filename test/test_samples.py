import pytest
import json


import requests

def test_new_samples():
    new_frag_file = open('new-fragility-set.json')
    new_frag = json.load(new_frag_file)

    print("=== new fragility ===")
    params = {'sample_size':2}
    response = requests.post('http://localhost:5000/api/samples', json=new_frag, params=params)
    print(response.content)

def test_old_samples():
    old_frag_file = open('old-fragility-set.json')
    old_frag = json.load(old_frag_file)

    print("=== old fragility ===")
    params = {'sample_size':2}
    response = requests.post('http://localhost:5000/api/samples', json=old_frag, params=params)
    print(response.content)


def test_3d_samples_response():
    with open('3d_fragility.json', 'r') as f:
        frag = json.load(f)
        response = requests.post('http://localhost:5000/api/samples', json=frag)
        print(response.content)


if __name__ == '__main__':
    test_new_samples()
