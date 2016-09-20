---
title: GI Bill Comparison Tool
date_added: 2015-11-01 00:00:00 -0500
vetsdotgov_url: https://www.vets.gov/gi-bill-comparison-tool/
status: normal
category: Discover
description: Now includes performance metrics on schools--and caution flags
before_jpg: gibct_old.png
after_jpg: gibct.png
tiles:

  - name: Mobile-first design
    layout: compare_donuts
    id: mobile
    datapoint: 100
    before: 46
    context: percentage of sites available on mobile

  - name: Veteran testimonial
    layout: quote
    text: The other website takes you around the corner, over the meadow, and...in a back door blocked with spikes and IEDs

  - name: Mobile availability
    layout: icon
    icon: smartphone.svg
    text: Veterans can now complete their application entirely from a smartphone

  - name: Site Traffic
    layout: chart
    data: gibct_users
    context: Total users per week
    cols:
      - id: all
        label: Count of users

  - name: Mobile Usage
    layout: chart
    data: gibct_mobile
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

  - name: New and Returning Users
    layout: chart
    data: gibct_new
    context: Count of users
    cols:
      - id: new
        label: New
        color: rgb(17,46,81)
      - id: returning
        label: Returning
        color: rgb(175,175,175)
---
