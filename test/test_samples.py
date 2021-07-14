import pytest
import json

import requests


def test_samples():
    old_frag_file = open('old-fragility-set.json')
    old_frag = json.load(old_frag_file)

    new_frag_file = open('new-fragility-set.json')
    new_frag = json.load(new_frag_file)

    print("=== new fragility ===")
    params = {'sample_size':2}
    response = requests.post('http://localhost:5000/api/samples', json=new_frag, params=params)
    print(response.content)

    # print("=== old fragility ===")
    # params = {'sample_size':2}
    # response = requests.post('http://localhost:5000/api/samples', json=old_frag, params=params)
    # print(response.content)


if __name__ == '__main__':
    test_samples()
