class MaxHeap:
    def __init__(self):
        self.heap = []
        self.entry_finder = {}
        self.REMOVED = '<removed>'
        self.counter = 0

    def add_score(self, username, user_score):
        if username in self.entry_finder:
            self.mark_removed(username)
        count = self.counter
        entry = [-user_score, count, username]
        self.entry_finder[username] = entry
        self.heap_push(entry)
        self.counter += 1

    def mark_removed(self, username):
        entry = self.entry_finder.pop(username)
        entry[-1] = self.REMOVED

    def pop_max(self):
        while self.heap:
            user_score, count, username = self.heap_pop()
            if username is not self.REMOVED:
                del self.entry_finder[username]
                return -user_score, username
        return None, None

    def heap_push(self, entry):
        self.heap.append(entry)
        self.upheap(len(self.heap) - 1)

    def heap_pop(self):
        last_entry = self.heap.pop()
        if self.heap:
            top_entry = self.heap[0]
            self.heap[0] = last_entry
            self.downheap(0)
            return top_entry
        return last_entry

    def upheap(self, pos):
        while pos > 0:
            parent_pos = (pos - 1) // 2
            if self.heap[pos] < self.heap[parent_pos]:
                self.swap(pos, parent_pos)
                pos = parent_pos
            else:
                break

    def downheap(self, pos):
        end_pos = len(self.heap)
        start_pos = pos
        new_item = self.heap[pos]
        child_pos = 2 * pos + 1
        while child_pos < end_pos:
            right_pos = child_pos + 1
            if right_pos < end_pos and self.heap[child_pos] > self.heap[right_pos]:
                child_pos = right_pos
            self.heap[pos] = self.heap[child_pos]
            pos = child_pos
            child_pos = 2 * pos + 1
        self.heap[pos] = new_item
        self.upheap(start_pos)

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    def current_size(self):
        return len(self.entry_finder)

    def is_empty(self):
        return len(self.entry_finder) == 0



class Leaderboard:
    def __init__(self):
        self.max_heap = MaxHeap()

    def update_score(self, username, user_score):
        self.max_heap.add_score(username, user_score)

    def show_leaderboard(self):
        temp_heap = MaxHeap()
        temp_heap.heap = self.max_heap.heap[:]
        temp_heap.entry_finder = self.max_heap.entry_finder.copy()
        temp_heap.counter = self.max_heap.counter

        print("Leaderboard:")
        rank = 1
        while not temp_heap.is_empty():
            user_score, username = temp_heap.pop_max()
            print(f"{rank}. {username}: {user_score} points")
            rank += 1
class Node2:
    def __init__(self, value=None):
        self.value = value
        self.next = None
        self.prev = None
class Deque:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, item):
        
        new_node = Node2(item)
        if self.tail is None:  # Deque is empty
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.size += 1

    def popleft(self):
        
        if self.head is None:
            raise IndexError("popleft from an empty deque")
        value = self.head.value
        self.head = self.head.next
        if self.head is None:  
            self.tail = None
        else:
            self.head.prev = None
        self.size -= 1
        return value
    
class Node:
    def __init__(self, name, course_credit):
        self.name = name
        self.course_credit = course_credit
        self.connections = []

    def add_edge(self, destination, credits):
        self.connections.append((destination, credits))

    def get_edges(self):
        return self.connections

class CourseGraph:
    def __init__(self):
        self.nodes = []
        self.edges={}
    def add_course(self, name, course_credit):
        for node in self.nodes:
            if node.name == name:
                return
        self.nodes.append(Node(name, course_credit))

    def add_edge(self, source, destination, credits):
        for node in self.nodes:
            if node.name == source:
                node.add_edge(destination, credits)
                break
        self.edges[(source,destination)]=credits

    def get_edges(self, node_name):
        for node in self.nodes:
            if node.name == node_name:
                return node.get_edges()
        return []

    def find_paths(self, start, end):
        queue = Deque()  
        queue.append([start])
        paths = []

        while queue.size>0:
            path = queue.popleft()
            node = path[-1]

            if node == end:
                paths.append(path)
            else:
                for connection, _ in self.get_edges(node):
                    if connection not in path:
                        new_path = list(path)
                        new_path.append(connection)
                        queue.append(new_path)

        return paths

    def calculate_path_credits(self, path):
        total_credits = 0
        for i in range(len(path) - 1):
            total_credits += self.edges.get((path[i], path[i + 1]), 0)  # Quick lookup of edge credits
        return total_credits

class CourseManager:
    def __init__(self):
        self.course_graph = CourseGraph()
        self.courses_with_credits = {
            'm1': 5, 'm2': 5, 'm3': 12,
            'p1': 5, 'p2': 5, 'p3': 5, 'p4': 6,
            'c1': 6, 'c2': 6, 'c3': 8, 'ch1': 7
        }
        self.users = {}
        self.logged_in_user = None
        self.leaderboard = Leaderboard()

    def setup_courses(self):
        for course, credits in self.courses_with_credits.items():
            self.course_graph.add_course(course, credits)

        edges = [
            ('m1', 'm2', 5), ('m1', 'm3', 12), ('m2', 'm3', 10),
            ('p1', 'p2', 5), ('p2', 'p3', 5), ('p2', 'p4', 5), ('p1', 'p4', 6), ('p3', 'p4', 10),
            ('c2', 'c1', 6), ('c3', 'c1', 8), ('c2', 'c3', 4), ('c3', 'c2', 7)
        ]

        for edge in edges:
            source, destination, credits = edge
            self.course_graph.add_edge(source, destination, credits)

        return True

    def suggest_courses(self):
        target_course = input("Enter the course you want to register for: ").strip()

        if target_course not in self.courses_with_credits:
            print(f"Error: The course '{target_course}' does not exist.")
            return

        paths = []
        for course in self.courses_with_credits:
            if course != target_course:
                paths.extend(self.course_graph.find_paths(course, target_course))

        if not paths:
            print(f"No path found to {target_course} from any other course.")
            print(f"You can directly study '{target_course}'")
            return

        max_total_credits = 0
        best_path = []
        for path in paths:
            total_credits = self.course_graph.calculate_path_credits(path)
            if total_credits > max_total_credits:
                max_total_credits = total_credits
                best_path = path

        print(f"Best path to {target_course} with the maximum total credits of {max_total_credits}:")
        print(best_path)

        confirm = input(f"Do you want to register for the path {best_path}? (yes/no): ").strip().lower()
        if confirm == 'yes':
            self.enroll_in_path(best_path)

        return best_path

    def enroll_in_path(self, path):
        if self.logged_in_user:
            registered_courses = self.users[self.logged_in_user]['courses']
            for course in path:
                if course in registered_courses:
                    print(f"Error: You have already registered for the course '{course}' in the path.")
                    print("The path is not possible since you have registered for one of the courses in the path individually.")
                    return

            total_credits = 0
            path_weight = 0

            for i in range(len(path)):
                self.users[self.logged_in_user]['courses'].add(path[i])
                credits = self.courses_with_credits[path[i]]
                total_credits += credits
                if i < len(path) - 1:
                    path_weight += self.course_graph.calculate_path_credits([path[i], path[i + 1]])

            total_credits += path_weight
            self.users[self.logged_in_user]['total_credits'] += total_credits
            self.leaderboard.update_score(self.logged_in_user, self.users[self.logged_in_user]['total_credits'])
            print(f"Path {path} registered for user '{self.logged_in_user}' successfully. Total credits earned: {total_credits}.")
        else:
            print("Please login first.")

    def create_account(self):
        username = input("Enter your username: ").strip()
        if username in self.users:
            print("Username already exists. Please choose another username.")
            return

        password = input("Enter your password: ").strip()
        self.users[username] = {'password': password, 'courses': set(), 'total_credits': 0}
        print(f"User '{username}' registered successfully.")

    def login_user(self):
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()
        if username not in self.users or self.users[username]['password'] != password:
            print("Invalid username or password.")
            return False
        else:
            print("Login successful!")
            self.logged_in_user = username
            return True

    def list_courses(self):
        print("Available Courses:")
        for course, credits in self.courses_with_credits.items():
            print(f"{course}: {credits} credits")

    def enroll_course(self):
        if self.logged_in_user:
            course_to_register = input("Enter the course you want to register for: ").strip()
            if course_to_register not in self.courses_with_credits:
                print(f"Error: The course '{course_to_register}' does not exist.")
                return
            registered_courses = self.users[self.logged_in_user]['courses']
            if course_to_register in registered_courses:
                print(f"Error: You have already registered for the course '{course_to_register}'.")
                return
            self.users[self.logged_in_user]['courses'].add(course_to_register)
            credits = self.courses_with_credits[course_to_register]
            self.users[self.logged_in_user]['total_credits'] += credits
            self.leaderboard.update_score(self.logged_in_user, self.users[self.logged_in_user]['total_credits'])
            print(f"Course '{course_to_register}' registered for user '{self.logged_in_user}' successfully. It has {credits} credits.")
        else:
            print("Please login first.")

    def show_registered_courses(self):
        if self.logged_in_user:
            registered_courses = self.users[self.logged_in_user]['courses']
            if registered_courses:
                print("Registered Courses:")
                for course in registered_courses:
                    credits = self.courses_with_credits[course]
                    print(f"{course}: {credits} credits")
                total_credits = self.users[self.logged_in_user]['total_credits']
                print(f"Total credits: {total_credits}")
            else:
                print(f"No registered courses found for user '{self.logged_in_user}'.")
        else:
            print("Please login first.")

    def show_total_credits(self):
        if self.logged_in_user:
            total_credits = self.users[self.logged_in_user]['total_credits']
            print(f"Total credits earned: {total_credits}")
        else:
            print("Please login first.")

    def show_leaderboard(self):
        self.leaderboard.show_leaderboard()

    def logout_user(self):
        self.logged_in_user = None
        print("Logged out successfully.")

    def main_menu(self):
        print("\nMenu:")
        print("1. Register")
        print("2. Login")
        print("3. View Leaderboard")
        print("4. Exit")

    def user_menu(self):
        print("\nUser Menu:")
        print("1. View available courses")
        print("2. Register for a course")
        print("3. View registered courses")
        print("4. Suggest courses")
        print("5. View total credits")
        print("6. View leaderboard")
        print("7. Logout")

    def run(self):
        if self.setup_courses():
            while True:
                self.main_menu()
                choice = input("Enter your choice: ").strip()
                if choice == '1':
                    self.create_account()
                elif choice == '2':
                    if self.login_user():
                        while True:
                            self.user_menu()
                            user_choice = input("Enter your choice: ").strip()
                            if user_choice == '1':
                                self.list_courses()
                            elif user_choice == '2':
                                self.enroll_course()
                            elif user_choice == '3':
                                self.show_registered_courses()
                            elif user_choice == '4':
                                self.suggest_courses()
                            elif user_choice == '5':
                                self.show_total_credits()
                            elif user_choice == '6':
                                self.show_leaderboard()
                            elif user_choice == '7':
                                self.logout_user()
                                break
                            else:
                                print("Invalid choice. Please enter a valid option.")
                elif choice == '3':
                    self.show_leaderboard()
                elif choice == '4':
                    print("Exiting...")
                    break
                else:
                    print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    manager = CourseManager()
    manager.run()