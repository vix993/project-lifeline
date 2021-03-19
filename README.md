# Lifeline:
## *Surviving an Apocalypse*

## Content

1. [Motivation](#Motivation) 
2. [Requirements](#Requirements)
3. [API](#API)
    - [Survivors](#Survivors)
    - [Flags](#Flags)
    - [Trades](#Trades)
    - [Reports](#Reports)
4. [Additional Notes](#API)

## Status

![Tests](https://github.com/vix993/project-lifeline/actions/workflows/test.yml/badge.svg)  ![Health Check](https://github.com/vix993/project-lifeline/actions/workflows/health_check.yml/badge.svg)

## Motivation

I was tasked with creating an API for the purpose of communication during a Zombie apocalypse.

What came out was [`Project Lifeline`](https://project-lifeline.herokuapp.com/).

With this application, survivors can register their details and inventories, update their location, flag other survivors as infected and execute trades.

There is also a reports endpoint for showing platform analysis.

You can run it with the following commands: 
- `git_clone https://github.com/vix993/project-lifeline.git`
- `cd project-lifeline`
- `python manage.py test` to run tests
- `install pip and virtualenv`
- `bash init.sh`
- It will perform the following:
    - `virtualenv django_env`
    - `source django_env/bin/activate`
    - `pip install -r requirements.txt`
    - `python manage.py makemigrations` + `python manage.py migrate`
    - `python manage.py runserver`

## Requirements

Django and djangorestframework were required for this project.

## Api
## *Survivors*

#### Create
Create new survivors & List the existing ones. Search using api/survivor/?q=my_search
##### Endpoint
`POST /api/survivor/`
##### Request parameter
`{"name":"jack", "age":"17", "gender":"M", "latitude":"40","longitude":"40","items":"Fiji Water:0;Campbell Soup:0;First Aid Pouch:0;AK47:4"}`
##### Response parameter
`{"name":"jack", "age":"17", "gender":"M", "latitude":"40","longitude":"40","items":"Fiji Water:0;Campbell Soup:0;First Aid Pouch:0;AK47:4"}`
#### Retrieve
Retrieve details of Survivor's
##### Endpoint
`GET /api/survivor/(pk)`
##### Query parameter
`pk` survivor id
##### Response parameter
`{
    "name":"jack", "age":"17", "gender":"M", "latitude":"40","longitude":"40",
    "items":"Fiji Water:0;Campbell Soup:0;First Aid Pouch:0;AK47:4", "infected": "True"
}`
#### Update
Update survivor location
##### Endpoint
`PUT /api/survivor/(pk)`
#### Request parameter
`{"latitude":"70","longitude":"60"}`
##### Query parameter
`pk` survivor id to be updated
##### Response parameter
`{
    "name":"jack", "age":"17", "gender":"M",
    "latitude":"70", "longitude":"60",
    "items":"Fiji Water:0;Campbell Soup:0;First Aid Pouch:0;AK47:4", "infected": "True"
}`

## *Flags*

#### Create
Create flags, suggesting that survivors are infected, incrementing their marks and confirming whether they have 5 accusations
##### Endpoint
`POST /api/survivor/flag/`
##### Request parameter
`{"flaged_pk":"1", "flager_pk":"2"}`
##### Response parameter
`{"pk":"1", "flaged_pk":"1", "flager_pk":"2"}`
#### Retrieve
Visualize flag history
##### Endpoint
`GET /api/survivor/flag/`

## *Trades*

#### Create
Create a trade request between two survivors if both parties have sufficient stock and the value of the requests is equal.
Update inventories if validation passes.
##### Endpoint
`POST /api/survivor/trade/`
##### Request Parameters
`{
    "seller_pk": "1",
    "buyer_pk": "2",
    "offered_items": "Fiji Water:0;Campbell Soup:2;First Aid Pouch:0;AK47:0",
    "requested_items": "Fiji Water:0;Campbell Soup:0;First Aid Pouch:0;AK47:3"
}`
##### Response Parameters
`{
    "seller_pk": "1",
    "buyer_pk": "2",
    "offered_items": "Fiji Water:0;Campbell Soup:2;First Aid Pouch:0;AK47:0",
    "requested_items": "Fiji Water:0;Campbell Soup:0;First Aid Pouch:0;AK47:3"
}`

## *Reports*

#### Retrieve, Update
Retrieve a report telling us some basic statistics about the current survivors
##### Endpoint
`GET /api/survivor/reports/`
##### Query parameter
There is only one reports object that will be updated on request at pk 1
##### Response parameter
`{
    "percentage_infected": "42.86%",
    "percentage_healthy": "57.14%",
    "average_water": "225.00 Fiji Waters per survivor.",
    "average_soup": "21.43 Campbell Soups per survivor.",
    "average_pouch": "74.57 First Aid Pouches per survivor.",
    "average_ak47": "196.43 AK47's per survivor.",
    "points_lost": "73240 points lost due to owner infection."
}`

## Additional Notes

1. API Endpoints -> registration, flags and reports
    - Search by case insensitive name 
        - .../postsurvivor/?q=your_search
    - Flag survivors as being infected
        - .../api/postsurvivor/flag/
        - Flags will update the flag count 
        of the accused survivor unless the same
        request already exists.
        - It will also update whether the flag confirms the person as infected (fifth strike).
    - Get reports on the survivor population
        - .../api/postsurvivor/flag/
        - Percentage of infected and non-infected survivors.
        - The average amount of resource per survivor
        - Points lost due to owner infection

2. API Endpoints -> marketplace tree
    - Post Trade Request:
        - This will verify whether either party is infected or do not have the required stock.
        Then it will ensure that the trade values are equal and execute the transaction, updating both inventories.
