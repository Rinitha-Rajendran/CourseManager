# CourseManager

CourseManager is an application designed to assist users in managing their course enrollments, tracking credits, and discovering optimal learning paths to achieve their educational goals effectively.

## Features

- **User Management**: Secure user registration and login system.
- **Course Management**: View available courses, enroll in courses, and track credits earned.
- **Leaderboard**: Dynamic leaderboard to foster competition among users based on total credits.
- **Course Suggestions**: Recommends optimal paths to achieve desired courses based on credit requirements.

## Getting Started

### Prerequisites

- Python 3.x
- Clone the repository:

  ```bash
  git clone https://github.com/Rinitha-Rajendran/CourseManager.git
  ```

### Installation

1. Navigate into the cloned directory:

   ```bash
   cd CourseManager
   ```

2. Run the main application:

   ```bash
   python course_manager.py
   ```

##Classes and Modules
**MaxHeap**
A custom implementation of a max-heap data structure, used to maintain the leaderboard efficiently.

**Leaderboard**
Manages the leaderboard using the MaxHeap class, allowing for dynamic updates and display.

**Deque**
A double-ended queue implementation used for breadth-first search (BFS) in the course suggestion system.

**Node and CourseGraph**
Represent the courses and their relationships. The graph structure helps in finding the optimal path between courses.

**CourseManager**
The main class that ties everything together. It handles user interactions, course enrollments, suggestions, and leaderboard updates.
## Usage

- Follow on-screen instructions to:
  - Register/login to your account.
  - Explore available courses and enroll in them.
  - View your registered courses and total credits earned.
  - Get course suggestions for optimal learning paths.
  - Check the leaderboard to see where you stand among other users.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your enhancements or bug fixes.


## Acknowledgments

- Built using Python, leveraging data structures and algorithms for efficient course management.
- Inspired by educational platforms aiming to enhance learning experiences.

##Future Enhancements
**Web Interface**: Develop a web-based interface for better accessibility.
**Database Integration**: Integrate with a database to persist user data and course information.
**Enhanced Security**: Implement more robust security measures for user authentication.

