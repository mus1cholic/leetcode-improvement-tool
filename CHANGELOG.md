
# Change Log
All notable changes to this project will be documented in this file.

## [0.3.1] - 2024-05-07
 
### Added

- Added changelog to keep track of changes
- Added multiple mongoDB collections
 
### Changed
  
- Changed build_question_rating_data method so that it completely uses mongoDB aggregate functions
- Changed layout of build_question_rating_data so that it also includes questions that aren't
currently in ratings.txt
 
### Fixed