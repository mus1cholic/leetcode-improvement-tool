# Change Log
All notable changes to this project will be documented in this file.

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