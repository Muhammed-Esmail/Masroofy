from datetime import timedelta

class DailyLimitCalculator:

    def getMoneySpent(self, transactions, cycle):
        '''
        ##Calculates total spent DURING this current cycle

        ### Parameters
        - transaction list : transactions
        - cycle : cycle

        ### Returns
        - a float 
        '''
        valid_transactions = [
            t for t in transactions 
            if cycle.startDate <= t.log_date <= cycle.endDate
        ]
        return sum(t.amount for t in valid_transactions)

    def getDaysLeft(self, currentDate, cycle):
        '''
        ## counts number of days left in current cycle (Including today)

        ### Parameters 
        - date : current_date
        - cycle : cycle

        ### Returns 
        - int (returns 1 if current date isn't in current cycle to prevent division by zero)
        '''
        delta = cycle.endDate - currentDate
        days = delta.days + 1
        return max(1, days)

    def getProjectedSpending(self, expenses, currentDate, cycle):
        '''
        ## calculates how much the user has to spend to cover his expenses in this current cycle

        ### Parameters
        - expense list : expenses
        - date : currentDate
        - cycle : cycle (current cycle)
        ### Returns
        - float 
        '''
        total = 0
        if currentDate > cycle.endDate:
            return 0
            
        days_remaining = (cycle.endDate - currentDate).days
        upcomingDates = [
            currentDate + timedelta(days=i) 
            for i in range(days_remaining + 1)
        ]
        
        weekdayMap = {0: 'MON', 1: 'TUE', 2: 'WED', 3: 'THU', 4: 'FRI', 5: 'SAT', 6: 'SUN'}

        for expense in expenses:
            occurrences = 0
            for checkDate in upcomingDates:
                if expense.frequency == 'MONTHLY' and checkDate.day in expense.days_of_month:
                    occurrences += 1
                elif expense.frequency == 'WEEKLY' and weekdayMap[checkDate.weekday()] in expense.days_of_week:
                    occurrences += 1
            total += (float(expense.amount) * occurrences)

        return total

    def calculateDailyLimit(self, currentDate, transactions, cycle, expenses):
        '''
        ## main daily limit calculate function. calls other class functions and calculates the limit.

        ### Parameters 
        - date : currentDate
        - transaction list : transactions
        - cycle : cycle
        - expense list : expenses

        ### Return
        - float
        '''
        money_in_cycle = cycle.amount 
        # Pass the cycle into our helper methods so they can do the filtering
        money_spent = self.getMoneySpent(transactions, cycle)
        days_left = self.getDaysLeft(currentDate, cycle)
        projected_spending = self.getProjectedSpending(expenses, currentDate, cycle)
        print("money", projected_spending)

        remaining_money = money_in_cycle - money_spent 
        remaining_money -= projected_spending
        
        daily_limit = remaining_money / days_left

        return max(0, daily_limit)