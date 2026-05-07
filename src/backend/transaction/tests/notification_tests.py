from typing import override

from django.test import TestCase
from history.services import *
from backend.shared_classes import *
from datetime import date
from transaction.services import NotificationManager, TransactionManager
from unittest.mock import patch
from backend.Controller import Controller
from transaction.constants import BUDGET_THRESHOLD_ALERT, BUDGET_EXHAUSTED_ALERT


class NotificationManagerTest(TestCase):
    @override
    def setUp(self):
        self.cycle_crud = CycleCRUD()
        self.category_crud = CategoryCRUD()
        self.transactionManager = TransactionManager()
        self.history_manager = HistoryManager()
        self.controller = Controller()
        self.notificationManager: NotificationManager = self.controller.getNotificationManager()

        self.sample_cycle = Cycle(
            id=None,
            startDate=date(2024, 1, 1),
            endDate=date(2024, 1, 31),
            amount=100
        )

        self.sample_category = Category(
            id=None,
            name="Clothing",
            description="Clothes Category"
        )

        self.sample_transaction = Transaction(
            id=None,
            amount=100,
            cycle_id=1,
            category_id=1,
            log_date=date(2006,6,6),
            description='KEFAYA B2A YA ESMAIL',
            note='OSAMA AYOHA EL LEADER EL 3ZEM, 8AREEB USES ARCH BTW'
        )

        self.active_cycle_id = self.cycle_crud.create(self.sample_cycle)
        self.category_crud.create(self.sample_category)
        self.history_manager.setActive(self.active_cycle_id)
    
    def test_threshold_80_alert(self):
        self.sample_transaction = Transaction(
            id=None,
            amount=80,
            cycle_id=self.active_cycle_id,
            category_id=1,
            log_date=date(2006, 6, 6),
            description='KEFAYA B2A YA ESMAIL',
            note='OSAMA AYOHA EL LEADER EL 3ZEM, 8AREEB USES ARCH BTW'
        )
        self.transactionManager.logTransaction(self.sample_transaction)

        with patch.object(self.notificationManager, 'triggerBudgetAlert') as mock_alert:
            self.notificationManager.update()
            mock_alert.assert_called_once_with(BUDGET_THRESHOLD_ALERT)
            
            
    def test_threshold_80_alert_update(self):
        self.sample_transaction = Transaction(
            id=1,
            amount=70,
            cycle_id=self.active_cycle_id,
            category_id=1,
            log_date=date(2006, 6, 6),
            description='KEFAYA B2A YA ESMAIL',
            note='OSAMA AYOHA EL LEADER EL 3ZEM, 8AREEB USES ARCH BTW'
        )
        self.transactionManager.logTransaction(self.sample_transaction)
        
        
        self.sample_transaction = Transaction(
            id=1,
            amount=90,
            cycle_id=self.active_cycle_id,
            category_id=1,
            log_date=date(2006, 6, 6),
            description='KEFAYA B2A YA ESMAIL',
            note='OSAMA AYOHA EL LEADER EL 3ZEM, 8AREEB USES ARCH BTW'
        )
        self.transactionManager.updateTransaction(self.sample_transaction)

        with patch.object(self.notificationManager, 'triggerBudgetAlert') as mock_alert:
            self.notificationManager.update()
            mock_alert.assert_called_once_with(BUDGET_THRESHOLD_ALERT)
            
        
    def test_budget_exhausted_alert(self):
        self.sample_transaction = Transaction(
            id=None,
            amount=101,
            cycle_id=self.active_cycle_id,
            category_id=1,
            log_date=date(2006, 6, 6),
            description='KEFAYA B2A YA ESMAIL',
            note='OSAMA AYOHA EL LEADER EL 3ZEM, 8AREEB USES ARCH BTW'
        )
        self.transactionManager.logTransaction(self.sample_transaction)

        self.notificationManager = self.controller.getNotificationManager()
        with patch.object(self.notificationManager, 'triggerBudgetAlert') as mock_alert:
            self.notificationManager.update()
            mock_alert.assert_called_once_with(BUDGET_EXHAUSTED_ALERT)
            
    def test_threshold_80_alert_trans_sum(self):
        self.sample_transaction = Transaction(
            id=None,
            amount=40,
            cycle_id=self.active_cycle_id,
            category_id=1,
            log_date=date(2006, 6, 6),
            description='KEFAYA B2A YA ESMAIL',
            note='OSAMA AYOHA EL LEADER EL 3ZEM, 8AREEB USES ARCH BTW'
        )
        
        self.sample_transaction_2 = Transaction(
            id=None,
            amount=50,
            cycle_id=self.active_cycle_id,
            category_id=1,
            log_date=date(2006, 6, 6),
            description='KEFAYA B2A YA ESMAIL',
            note='OSAMA AYOHA EL LEADER EL 3ZEM, 8AREEB USES ARCH BTW'
        )
        
        self.transactionManager.logTransaction(self.sample_transaction)
        self.transactionManager.logTransaction(self.sample_transaction_2)

        with patch.object(self.notificationManager, 'triggerBudgetAlert') as mock_alert:
            self.notificationManager.update()
            mock_alert.assert_called_once_with(BUDGET_THRESHOLD_ALERT)
            
            
    def test_exhausted_alert_trans_sum(self):
        self.sample_transaction = Transaction(
            id=None,
            amount=40,
            cycle_id=self.active_cycle_id,
            category_id=1,
            log_date=date(2006, 6, 6),
            description='KEFAYA B2A YA ESMAIL',
            note='OSAMA AYOHA EL LEADER EL 3ZEM, 8AREEB USES ARCH BTW'
        )
        
        self.sample_transaction_2 = Transaction(
            id=None,
            amount=80,
            cycle_id=self.active_cycle_id,
            category_id=1,
            log_date=date(2006, 6, 6),
            description='KEFAYA B2A YA ESMAIL',
            note='OSAMA AYOHA EL LEADER EL 3ZEM, 8AREEB USES ARCH BTW'
        )
        
        self.transactionManager.logTransaction(self.sample_transaction)
        self.transactionManager.logTransaction(self.sample_transaction_2)

        with patch.object(self.notificationManager, 'triggerBudgetAlert') as mock_alert:
            self.notificationManager.update()
            mock_alert.assert_called_once_with(BUDGET_EXHAUSTED_ALERT)           
            

    def test_below_threshold_no_alert(self):
        self.sample_transaction = Transaction(
            id=None,
            amount=79,
            cycle_id=self.active_cycle_id,
            category_id=1,
            log_date=date(2006, 6, 6),
            description='KEFAYA B2A YA ESMAIL',
            note='OSAMA AYOHA EL LEADER EL 3ZEM, 8AREEB USES ARCH BTW'
        )
        self.transactionManager.logTransaction(self.sample_transaction)

        self.notificationManager = self.controller.getNotificationManager()
        with patch.object(self.notificationManager, 'triggerBudgetAlert') as mock_alert:
            self.notificationManager.update()
            mock_alert.assert_not_called()
            
            
    def test_below_threshold_no_alert_delete(self):
        self.sample_transaction = Transaction(
            id=1,
            amount=30,
            cycle_id=self.active_cycle_id,
            category_id=1,
            log_date=date(2006, 6, 6),
            description='KEFAYA B2A YA ESMAIL',
            note='OSAMA AYOHA EL LEADER EL 3ZEM, 8AREEB USES ARCH BTW'
        )
        self.transactionManager.logTransaction(self.sample_transaction)
        
        self.transactionManager.deleteTransaction(self.sample_transaction.id)

        self.notificationManager = self.controller.getNotificationManager()
        with patch.object(self.notificationManager, 'triggerBudgetAlert') as mock_alert:
            self.notificationManager.update()
            mock_alert.assert_not_called()
            
            
    def test_below_threshold_no_alert_trans_sum(self):
        self.sample_transaction = Transaction(
            id=None,
            amount=10,
            cycle_id=self.active_cycle_id,
            category_id=1,
            log_date=date(2006, 6, 6),
            description='KEFAYA B2A YA ESMAIL',
            note='OSAMA AYOHA EL LEADER EL 3ZEM, 8AREEB USES ARCH BTW'
        )
        
        self.sample_transaction_2 = Transaction(
            id=None,
            amount=20,
            cycle_id=self.active_cycle_id,
            category_id=1,
            log_date=date(2006, 6, 6),
            description='KEFAYA B2A YA ESMAIL',
            note='OSAMA AYOHA EL LEADER EL 3ZEM, 8AREEB USES ARCH BTW'
        )
        self.transactionManager.logTransaction(self.sample_transaction)
        self.transactionManager.logTransaction(self.sample_transaction_2)

        self.notificationManager = self.controller.getNotificationManager()
        with patch.object(self.notificationManager, 'triggerBudgetAlert') as mock_alert:
            self.notificationManager.update()
            mock_alert.assert_not_called()