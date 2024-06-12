# Change Log
All notable changes to this project will be documented in this file.

## [0.5.5] - 2024-06-11

### Added

- Added full functionality for advanced recommendation options

### Changed

### Fixed

- Fixed bug with rating filter that caused the search to default to a moderate
problem when the ratings weren't specified

## [0.5.4] - 2024-06-10

### Added

- Added some functionality for advanced recommendation options, the filtering
out of user completed questions as well as the random choice will come in
the next update

### Changed

### Fixed

## [0.5.3] - 2024-06-08

### Added

- Added leetcode profile icon when doing /profile

### Changed

### Fixed

- Fixed search term modal causing an error

## [0.5.2] - 2024-06-07

### Added

- Added a separate cog for general/utility commands

### Changed

- Changed /advancerecommend command to use a custom View to select options

### Fixed

## [0.5.1] - 2024-06-01

### Added

- Added profile embed through /profile command

### Changed

### Fixed

## [0.5.0] - 2024-05-30

### Added

- Added a few utility functions
- Added virtual environment for easier management of packages

### Changed

- Changed database to use ML model's rating if rating not in ratings.txt

### Fixed

- Fixed logic of parsing ratings from ratings.txt

## [0.4.5] - 2024-05-29

### Added

- Successfully set up environment on AWS E2 instance
- Added requirements.txt
 
### Changed
 
### Fixed

## [0.4.4] - 2024-05-28

### Added

- Added server logo
- Added various indexes to database to speed up query process
- Added submission/accepted data in database
- Added Gradient Boosting Model with RMSE of ~175 to predict rating
of questions not in ratings.txt. The model and parameters are kept
private and will only be used to obtain rating data for some of
the earlier questions that ratings.txt doesn't cover
 
### Changed
 
### Fixed

## [0.4.3] - 2024-05-13

### Added

- Added total functionality of blacklisting some of your tags to never
see a problem with a certain tag
 
### Changed

- Changed naming of preferences to settings for clearer idea
- Changed tags field of rating question tag db to be consistent (using an array of slugs)
 
### Fixed

- Fixed build_preferences() method not being called in Users.py
- Fixed fstring for recommending a problem

## [0.4.2] - 2024-05-12
 
### Added

- Added a mention whenever users gets recommended a problem
- Added frontend UI of removing/adding tags to your recommendation list
- Added Profile class with no functionality
 
### Changed

- Changed user creation to also include saving preferences
 
### Fixed

## [0.4.1] - 2024-05-10
 
### Added

- Added functionality for a simple recommend
- Added a check for a completely new profile with no questions done
 
### Changed

- Changed db init design to use a standalone client class instead of being initialized
in individual files
 
### Fixed

## [0.4.0] - 2024-05-09
 
### Added

- Added full implementation for user to upload their data to db
- Added user class to deal with complicated logics for a user
- Added contest ratings and projected ratings
 
### Changed

- Changed question_id field in rating_question_tag_data collection to be of type int
- Changed Tags class to use enum
- Changed Tags class methods to use mongoDB
 
### Fixed

## [0.3.2] - 2024-05-08
 
### Added

- Added docstrings in method descriptions to show up in discord's
command system
 
### Changed

- Changed /createprofile and /updateprofile command to support attachment
uploads
- Changed some of build_user_data method and logics to use database instead of local files,
exact implementation will be done in next update
- Changed check_user_exist method to use self
 
### Fixed

- Fixed /createprofile command using Builder class and moved Builder object
initialization to class init method

## [0.3.1] - 2024-05-07
 
### Added

- Added changelog to keep track of changes
- Added multiple mongoDB collections
 
### Changed
  
- Changed build_question_rating_data method so that it completely uses mongoDB aggregate functions
- Changed layout of build_question_rating_data so that it also includes questions that aren't
currently in ratings.txt
 
### Fixed