from psycopg2._psycopg import Error

from Terminal import ManagerQueries
from Terminal.Terminal import Terminal


class ManagerTerminal(Terminal):
    def manager_main(self):
        Terminal.fancy_print("Welcome back " + self.current_username + "!", "Choose one of these options:"
                             , '[1] Add new flight'
                             , '[2] Add/Remove airplane'
                             , '[3] User\'s comments'
                             , '[4] Giving discount to users'
                             , '[5] Customers list based on number of travels'
                             , '[6] Target city list'
                             , '[7] Airplanes list in a city'
                             , '[8] Analyzing scores'
                             , '[9] See entity lists'
                             , '[10] Give salary to employees'
                             )
        query = int(input())
        if query == 1:
            self.manager_add_flight()
        elif query == 2:
            self.manager_add_remove_airplane()
        elif query == 3:
            self.manager_user_comments()
        elif query == 4:
            self.manager_give_discount()
        elif query == 5:
            self.manager_customer_list_by_travels()
        elif query == 6:
            self.manager_target_city_list()
        elif query == 7:
            self.manager_airplane_list_in_city()
        elif query == 8:
            self.manager_scores()
        elif query == 9:
            self.manager_entity_lists()
        elif query == 10:
            self.manager_give_salaries()

    def manager_add_flight(self):
        all_flights = self.execute_database_query(ManagerQueries.get_all_flight_query())
        new_code = len(all_flights)
        Terminal.fancy_print('Enter Following Information:',
                             'Time (YYYY-MM-DD HH:MM:SS)',
                             'Starting city',
                             'Target city',
                             'Ticket price',
                             'Airplane code',
                             'Captain code')
        time = input()
        starting_city = input()
        target_city = input()
        ticket_price = int(input())
        airplane_code = int(input())
        captain_code = int(input())

        try:
            self.execute_database_query(ManagerQueries.get_add_flight_query(new_code, time, starting_city, target_city,
                                                                            ticket_price, airplane_code, captain_code))
            print("Flight added successfully!")
        except (Exception, Error) as error:
            print("Error while inserting new flight", error)

        self.manager_back_to_main()

    def manager_back_to_main(self):
        print("----------\nPress Y to go back!")
        tmp = input()
        self.manager_main()

    def manager_add_airplane(self):
        all_airplanes = self.execute_database_query(ManagerQueries.get_all_airplanes_query())
        new_code = len(all_airplanes)
        Terminal.fancy_print('Enter following information:',
                             'Capacity', 'Model', 'CIty')
        cap = int(input())
        model = input()
        city = input()
        try:
            self.execute_database_query(
                ManagerQueries.get_add_airplane_query(new_code, cap, model, city))
            print("Airplane added successfully!")
        except (Exception, Error) as error:
            print("Error while inserting new airplane", error)

        self.manager_back_to_main()

    def manager_remove_airplane(self):
        Terminal.fancy_print('Enter airplane\'s code')
        code = int(input())
        try:
            self.execute_database_query(
                ManagerQueries.get_remove_airplane_query(code))
            print("Airplane removed successfully!")
        except (Exception, Error) as error:
            print("Error while removing airplane", error)

        self.manager_back_to_main()

    def manager_add_remove_airplane(self):
        Terminal.fancy_print("[1] Add an airplane", '[2] Remove airplane')
        query = int(input())
        if query == 1:
            self.manager_add_airplane()
        else:
            self.manager_remove_airplane()

    def manager_user_comments(self):
        try:
            all_comments = self.execute_database_query(
                ManagerQueries.get_all_comments_query())
            print(all_comments)
        except (Exception, Error) as error:
            print("Error while fetching comments", error)

        self.manager_back_to_main()

    def manager_give_discount(self):
        Terminal.fancy_print('Enter user\'s NC', 'Discount No',
                             'Discount Percent', 'Expiration time (YYYY-MM-DD HH:MM:SS)')

        nc = input()
        discount_no = input()
        percent = int(input())
        expiration_time = input()
        try:
            self.execute_database_query(
                ManagerQueries.get_add_discount_query(nc, discount_no,
                                                      percent, expiration_time))
            print('Giving discount successful')
        except (Exception, Error) as error:
            print("Error while inserting discount", error)

        self.manager_back_to_main()

    def manager_target_city_list(self):
        try:
            cities = self.execute_database_query(
                ManagerQueries.get_target_city_query())

            print(cities)  # TODO print?
        except (Exception, Error) as error:
            print("Error while fetching target city data", error)

        self.manager_back_to_main()

    def manager_airplane_list_in_city(self):
        Terminal.fancy_print("Enter city name:")
        city = input()
        try:
            airplanes = self.execute_database_query(
                ManagerQueries.get_airplanes_in_city_query(city))
            print(airplanes)  # TODO print?
        except (Exception, Error) as error:
            print("Error while fetching airplanes", error)

        self.manager_back_to_main()

    def manager_score_employees(self):
        try:
            employees = self.execute_database_query(
                ManagerQueries.get_employee_score_query())
            print(employees)  # TODO print?
        except (Exception, Error) as error:
            print("Error while fetching employees\' scores", error)

        self.manager_back_to_main()

    def manger_score_airplanes(self):
        try:
            airplanes = self.execute_database_query(
                ManagerQueries.get_airplane_score_query())
            print(airplanes)  # TODO print?
        except (Exception, Error) as error:
            print("Error while fetching airplanes\' scores", error)

        self.manager_back_to_main()

    def manager_score_captains(self):
        try:
            captains = self.execute_database_query(
                ManagerQueries.get_captains_score_query())
            print(captains)  # TODO print?
        except (Exception, Error) as error:
            print("Error while fetching captains\' scores", error)

        self.manager_back_to_main()

    def manager_scores(self):
        Terminal.fancy_print('[1] See employees\' scores',
                             '[2] See airplanes\' scores',
                             '[3] See captains\' scores')
        query = input()
        if query == '1':
            self.manager_score_employees()
        elif query == '2':
            self.manger_score_airplanes()
        else:
            self.manager_score_captains()

    def manager_customer_list_by_travels(self):
        try:
            all_customers = self.execute_database_query(
                ManagerQueries.get_customers_by_travels())

            print(all_customers)  # TODO print?
        except (Exception, Error) as error:
            print("Error while fetching customers\' travels", error)

        self.manager_back_to_main()

    def manager_customer_list(self):
        try:
            all_customers = self.execute_database_query(
                ManagerQueries.get_all_customers_query())

            print(all_customers)  # TODO print?
        except (Exception, Error) as error:
            print("Error while fetching customers", error)

        self.manager_back_to_main()

    def manager_airplane_list(self):
        try:
            all_airplanes = self.execute_database_query(
                ManagerQueries.get_all_airplanes_query())

            print(all_airplanes)  # TODO print?
        except (Exception, Error) as error:
            print("Error while fetching airplanes", error)

        self.manager_back_to_main()

    def manager_employee_list(self):
        try:
            all_employees = self.execute_database_query(
                ManagerQueries.get_all_employees_query())

            print(all_employees)  # TODO print?
        except (Exception, Error) as error:
            print("Error while fetching employees", error)

        self.manager_back_to_main()

    def manager_travel_list(self):
        try:
            all_travels = self.execute_database_query(
                ManagerQueries.get_all_travels_query())

            print(all_travels)  # TODO print?
        except (Exception, Error) as error:
            print("Error while fetching travels", error)

        self.manager_back_to_main()

    def manager_entity_lists(self):
        Terminal.fancy_print('[1] See customers',
                             '[2] See airplanes',
                             '[3] See employees',
                             '[4] See travels')
        query = input()
        if query == '1':
            self.manager_customer_list()
        elif query == '2':
            self.manager_airplane_list()
        elif query == '3':
            self.manager_employee_list()
        else:
            self.manager_travel_list()

    def manager_give_salaries(self):
        try:
            self.execute_database_query(
                ManagerQueries.get_give_salary_query())
            print("Giving salaries successful")
        except (Exception, Error) as error:
            print("Error while giving salaries", error)

        self.manager_back_to_main()
