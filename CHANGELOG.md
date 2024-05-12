# Change Log
All notable changes to this project will be documented in this file.

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