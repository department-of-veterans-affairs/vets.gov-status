# Vets.gov Executive Scorecard

> A scorecard for vets.gov projects

The executive scorecard is meant to provide a simple overview of the vets.gov project to external audiences. It is often used in briefings but should be able to stand-alone with enough context offered for a visitor unfamiliar with vets.gov to navigate it and understand it.

## Structure

### Landing page

The executive scorecard has a main landing page `index.html` that provides the vets.gov vision statement as context for the project.

The six most important data points on the impact of vets.gov are presented in a set of "tiles." These are rotated and may be customized for ahead of briefings to key stakeholders.

A set of summary metrics over time are conveyed in series of charts in a tab group. The metrics are presented as weekly data to smooth out some of the day-to-day variance and provide a long-term trend view. The tabs are used to conserve visual space. The data for the charts is pulled in at build time from csv files in the `_data` directory. Those csv files are updated using Python scripts in `scripts` directory.

Each significant feature or function of vets.gov gets its own "tile" in the project section. They are grouped by which of the parts of vision statement they fulfill. Completed features are links to detailed scorecard boards. "Coming soon" features can also be displayed. This section is constructed at build time from the contents of the `_board` directory.

There are special call-out sections for the human-centered design work and progress of migrations.

### Detailed Project Boards

Each feature or function gets its own board in `_board` directory. It has a project overview section, followed by up to three data 'tiles' of key facts, a set of charts, and before/after screenshots.

The boards are generated from the yaml front matter in each Markdown file. The actual content in the Markdown is not used and should be omitted.

#### Feature/Function Board Fields
- title: The name of the feature/function [Required]
- date_added: When the feature/function launched [Optional]
- vetsdotgov_url: URL on production site [Optional]
- status: `normal` for launched items, `progress` for 'coming soon' items [Required]
- category: Which of the vision statement categories it belongs in: `Discover`, `Apply`, `Track`, `Manage` [Required]
- description: One sentence description, will display on the landing page [Required]
- extended_description: Will replace description on detailed page if supplied [Optional]
-screenshot: The file base name for screenshots. If `basename` is entered here, there should be `assets\img\basename.png` for the after and `assets\img\basename_old.png` provided. `placeholder` can be used if no screenshots are ready. [Required]
-tiles: A list of up to three data `tiles` to display. Some examples are in `showcase.html` or check the actual html for each in `_includes\tiles`. [Required]
-clicks: Will display an "Outbound links" chart for tracking traffic sent to other sites
-charts: The file base name for the data charts in `_data` and should match what is used in `scripts\config.json`

## Chart data

The charts are powered by the vets.gov Google Analytics account. The Python scripts in `scripts` pull data from the Google Analytics account and create a set of updated CSV files in `_data` that are then used by Jekyll to build the actual charts.

Once deployed the data is static until the next deploy. Because the executive scorecard is meant for external audiences, this ensures that the data is available and can be quality controlled prior to putting it in front of an audience. Once deployed, we do not have to worry about data abnormalities or failures appearing.

## Getting started

1. Install Ruby if needed (MacOS has by default)
1. Install [Jekyll](https://jekyllrb.com/docs/installation/)
2. Clone this repository to your local computer
3. Run `bundle` to install gems
3. Serve the project locally
  ```
  bundle exec jekyll serve
  ```

## Deploying

Our deployments are handled by Jenkins using the `Jenkinsfile`. We deploy by committing to the `production` branch. We use the `demo` branch to deploy to our development server to internally demo new boards or tile updates without blocking the data update path from `master` to `production`.

## Previous repo

This repo previously held a now defunct dashboard. The prior work is archived as a release on this repo in case that work needs to be revisited.
