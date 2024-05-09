# [Task 1](/docs/task1.md#table-of-contents) / TASK 2 - Solution

TAG `task2`

## Description

A new endpoint for `no-staff` users to send a change request to an existing hotel.
When the changes are sent, `reviewer` users are notified by email to approve or reject the request.
For this operation, the Django admin interface is used. In it, the reviewer can approve, reject, or delete the request, both from the detail view and the list of requests.
To approve the request, a form is launched in which the proposed changes and the current version can be viewed.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Table of Contents

- [Admin View](#admin-view)
- [Settings](#settings)
  - [Configuration Variables](#configuration-variables)
- [Components](#components)
  - [Endpoints](#endpoints)
- [Models](#models)
  - [Serializers](#serializers)
  - [Views](#views)
  - [Admin](#admin)
  - [Signals](#signals)
  - [Managers](#managers)
- [Business Logic](#business-logic)
- [Technical Debt](#technical-debt)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Admin View

The admin view has been customized with bulk actions to reject and put requests on hold, as well as to activate and deactivate hotels.
In the hotel chains view, you can create hotels inline.
In the draft hotel view, you can approve or reject change requests, if it is an existing request, the action buttons should appear.
See the images of the [admin view](admin.md).

## Settings

### Configuration Variables

The `HOTEL_LOCATIONS` configuration variable has been added to define the cities of the hotels. In case more cities are required, a model should be created for the cities and related to the hotels. I have assumed that there are few entries and that the `location` field refers only to cities.

```python
HOTEL_LOCATIONS = [
    ('madrid', 'Madrid'),
    ('barcelona', 'Barcelona'),
    ('sevilla', 'Sevilla'),
]
```

## Components

### Endpoints

The API has the following endpoints:

- `/admin/`: Django Admin
- `/api/v1/hotels/`: CRUD of hotels
- `/api/v1/hotelchains/`: CRUD of hotel chains
- `/api/v1/hoteldrafts/`: CRUD of hotel drafts

- Auto documentation
  - `/api/v1/`: Swagger
  - `/api/v1/redocs/`: Redocs

- JWT
  - `/api/v1/token/`: Obtain token
  - `/api/v1/token/refresh/`: Refresh token
  - `/api/v1/token/verify/`: Verify token

For more information on the API endpoints, you can access the API documentation at `/api/v1/redoc`.

## Models

Models have been defined for the API:

- `AbstractHotel`: Abstract model to store common fields for:
  - `Hotel`: Model to store hotel information
  - `HotelDraft`: Model to store hotel draft information
- `HotelChain`: Model to store hotel chain information

### Serializers

Serializers have been defined for the API models:

- `HotelSerializer`: Serializer for the model `Hotel`
- `HotelChainSerializer`: Serializer for the model `HotelChain`
- `HotelDraftSerializer`: Serializer for the model `HotelDraft`

### Views

Views have been defined for the API models:

- `HotelViewSet`: View for the `Hotel` model
- `HotelChainViewSet`: View for the `HotelChain` model
- `HotelDraftViewSet`: View for the `HotelDraft` model

### Admin

Admins have been defined for the API models:

- `HotelAdmin`: Admin for the model `Hotel`
- `HotelChainAdmin`: Admin for the model `HotelChain`

### Signals

Signal handlers have been defined for the API models:

- `hotel_signal_pre_save`: Signal to auto-assign a hotel chain to a hotel
- `hotel_signal_post_save`: Signal to relate hotels according to the business logic and send an email notification
- `hotel_chain_signal_pre_save`: Signal to format the title of the hotel chain before saving it
- `hotel_draft_signal_post_save`: Signal to send an email notification to the reviewers when a draft is created

### Managers

Mangers have been defined for the API models:

- `AbstrtactHotelManager`: Manager for the `AbstractHotel` model
  - `nested_create`: Method to create hotels with nested hotel chains.
  - `nested_update`: Method to update a hotel with nested hotel. (_No Implemented Yet_)

- `HotelChainManager`: Manager for the `HotelChain` model
  - `create`: Method to create a hotel chain and keep the `title` field unique.
  - `filter_by_title_with_auto_assign`: Method to filter hotel chains by title and assign a hotel to the chain if it exists.

## Business Logic

The business logic of the API is as follows:

- A hotel can belong to a single hotel chain or not belong to any hotel chain.
- If a hotel chain is marked as auto_assign, when a hotel is created a logic will be applied:
  - the title of the chain is contained in the name of the hotel
  - the title of the string is more than 3 characters
  - the hotel does not have an assigned chain
- When a hotel is created if it has a chain assigned, it will be notified by email if it has an email for it.
- A hotel is related to other hotels if they belong to the same chain.
- A hotel is related to other hotels if they belong to the same chain.
- A hotel chain is created if its title is unique; otherwise, the existing hotel chain is returned.
- The title of a hotel chain is formatted as "title" before saving. Example: "hotel chain", "HoTel ChAiN" -> "Hotel chain"
- For `api/v1/hotels/` only `staff` users can update hotels.
  - `no-staff` users can send change requests to existing hotels through `api/v1/hoteldrafts/`.
  - `reviewer` users can approve or reject change requests through the Django admin interface.
![Logic](/docs/assets/draft_hotel.jpg)

## Technical Debt

I could not do it due to lack of time, but it can be done in the future.

- [ ] Implement the `nested_update` method in the `AbstrtactHotelManager` manager.
- [ ] Implement `GH_ACTION` for CI/CD.
