---
title: Facility Locator
date_added:
vetsdotgov_url: https://www.vets.gov/facility-locator/
status: normal
category: Discover
description: Veterans can search facilities AND VA services!
before_jpg: facility_old.png
after_jpg: facility.png
tiles:

  - name: Fixed for Veterans who are blind or have low-vision
    layout: basic
    datapoint: 79
    context: accessibility issues from prior locators

  - name: Integrated directions
    layout: icon
    icon: road
    text: Connects with Google Maps to provide driving and public transit directions

  - name: Locators being consolidated
    layout: compare
    datapoint: 1
    before: 43

  - name: <span class="glyphicon glyphicon-user tab-icon" aria-hidden="true"></span><span>Users</span>
    layout: chart
    data: facility_users
    context: Total users per week
    cols:
      - id: all
        label: Count of users

  - name: <span class="glyphicon glyphicon-phone tab-icon" aria-hidden="true"></span><span>Mobile Use</span>
    layout: chart
    data: facility_mobile
    context: Percentage of users by device type used
    yLabel: Percentage
    yMax: 100
    cols:
      - id: mobile
        label: Mobile
        color: rgb(17,46,81)
      - id: desktop
        label: Desktop
        color: rgb(175,175,175)

  - name: <span class="glyphicon glyphicon-file tab-icon" aria-hidden="true"></span><span>Views</span>
    layout: chart
    data: facility_views
    context: Total page views per week
    cols:
      - id: views
        label: Count of pageviews
---
