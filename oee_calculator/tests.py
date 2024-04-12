# tests.py

from django.test import TestCase
from django.urls import reverse
from .models import Machine, ProductionLog
import datetime

class MachineModelTestCase(TestCase):
    def setUp(self):
        self.machine = Machine.objects.create(machine_name='Machine 1', machine_serial_no='123456')

    def test_machine_creation(self):
        self.assertEqual(self.machine.machine_name, 'Machine 1')
        self.assertEqual(self.machine.machine_serial_no, '123456')

class OEECalculationTestCase(TestCase):
    def setUp(self):
        # Create sample data
        self.machine = Machine.objects.create(machine_name='Machine 1', machine_serial_no='123456')
        self.start_time = datetime.datetime.now() - datetime.timedelta(hours=1)
        self.end_time = datetime.datetime.now()
        self.production_log = ProductionLog.objects.create(cycle_no='CN001', unique_id='ID001',
                                                            material_name='Material A', machine=self.machine,
                                                            start_time=self.start_time, end_time=self.end_time,
                                                            duration=(self.end_time - self.start_time).total_seconds() / 3600)

    def test_oee_calculation(self):
        # Calculate OEE for the sample data
        available_time = 24
        unplanned_downtime = 2
        ideal_cycle_time = 5
        actual_output = 1  # Assuming only 1 product produced
        good_products = 1  # Assuming only 1 good product
        total_products = 1  # Assuming only 1 product produced

        # Calculate availability, performance, and quality as percentages
        availability = ((available_time - unplanned_downtime) / available_time) * 100
        performance = (ideal_cycle_time * actual_output) / (self.production_log.duration) * 100
        quality = (good_products / total_products) * 100

        # Calculate OEE (convert to percentage)
        expected_oee = (availability * performance * quality) / 10000

        # Get OEE from the API
        response = self.client.get(reverse('oee_data'))
        self.assertEqual(response.status_code, 200)
        # Assert the calculated OEE with a delta
        self.assertAlmostEqual(response.json()['oee'], expected_oee, delta=0.01)

# class OEEAPITestCase(TestCase):
#     def setUp(self):
#         self.machine = Machine.objects.create(machine_name='Machine 1', machine_serial_no='123456')

#     def test_oee_api(self):
#         # Create sample data
#         start_time = datetime.datetime.now() - datetime.timedelta(hours=1)
#         end_time = datetime.datetime.now()
#         production_log = ProductionLog.objects.create(cycle_no='CN001', unique_id='ID001',
#                                                       material_name='Material A', machine=self.machine,
#                                                       start_time=start_time, end_time=end_time,
#                                                       duration=(end_time - start_time).total_seconds() / 3600)

#         # Test endpoint with filter
#         response = self.client.get(reverse('oee_data'))
#         self.assertEqual(response.status_code, 200)
#         # Adjust the assertion to expect a length of 1
#         self.assertEqual(len(response.json()), 1)
