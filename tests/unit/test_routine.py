import unittest 
from unittest.mock import Mock
from edge.core.state.Step import Step
from edge.core.state.Routine import Routine
from edge.core.enums.ActionEnums import CommandAction
from edge.core.models.RuntimeContext import RuntimeContext

class TestRoutineCommandReportsSuccess(unittest.TestCase):
  def test_command_chain(self):
    report = _mock_report(report_ok=True, isRunning=False)
    command = _mock_command(report)
    steps = [Step(command)]
    TestRoutine = Routine(steps=steps, verbose=False)
    TestRuntimeContext: RuntimeContext = TestRoutine.run()

    self.assertEqual(len(TestRuntimeContext.reports["chain_id_0"]), 1)
    self.assertTrue(TestRuntimeContext.reports["chain_id_0"][0].ok)
    self.assertIsNone(TestRuntimeContext.terminated_by)
    self.assertIsNone(TestRuntimeContext.terminated_at_chain_id)

class TestRoutineCommandReportsFailed(unittest.TestCase):
  def test_command_chain(self):
    report = _mock_report(report_ok=False, isRunning=False)
    command = _mock_command(report)
    steps = [Step(command)]
    TestRoutine = Routine(steps=steps, verbose=False)
    TestRuntimeContext: RuntimeContext = TestRoutine.run()

    self.assertEqual(len(TestRuntimeContext.reports["chain_id_0"]), 1)
    self.assertFalse(TestRuntimeContext.reports["chain_id_0"][0].ok)
    self.assertIsNone(TestRuntimeContext.terminated_by)
    self.assertIsNone(TestRuntimeContext.terminated_at_chain_id)

class TestRoutineCommandReportsSuccessIsRunningTrue(unittest.TestCase):
  def test_command_chain(self):
    report = _mock_report(report_ok=True, isRunning=True)
    command = _mock_command(report)
    steps = [Step(command)]
    TestRoutine = Routine(steps=steps, verbose=False)
    TestRuntimeContext: RuntimeContext = TestRoutine.run()

    self.assertEqual(len(TestRuntimeContext.reports["chain_id_0"]), 1)
    self.assertTrue(TestRuntimeContext.reports["chain_id_0"][0].ok)
    self.assertIsNone(TestRuntimeContext.terminated_by)
    self.assertIsNone(TestRuntimeContext.terminated_at_chain_id)

class TestRoutineCommandReportsFailedChainEvaluatorActionAbort(unittest.TestCase):
  def test_command_chain(self):
    report = _mock_report(report_ok=False, isRunning=False)
    command = _mock_command(report)
    steps = [Step(command).on_failure_do(CommandAction.ABORT)]
    TestRoutine = Routine(steps=steps, verbose=False)
    TestRuntimeContext: RuntimeContext = TestRoutine.run()

    self.assertEqual(len(TestRuntimeContext.reports["chain_id_0"]), 1)
    self.assertFalse(TestRuntimeContext.reports["chain_id_0"][0].ok)
    self.assertEqual(TestRuntimeContext.terminated_by, CommandAction.ABORT)
    self.assertEqual(TestRuntimeContext.terminated_at_chain_id, 0)

class TestRoutineCommandReportsFailedChainEvaluatorNotRunningDoSuccess(unittest.TestCase):
  def test_command_chain(self):
    command_a_report = _mock_report(report_ok=False, isRunning=False)
    command_b_report = _mock_report(report_ok=True, isRunning=None)
    command_a = _mock_command(command_a_report)
    command_b = _mock_command(command_b_report)
    steps = [Step(command_a).not_running_do(command_b)]
    TestRoutine = Routine(steps=steps, verbose=False)
    TestRuntimeContext: RuntimeContext = TestRoutine.run()

    self.assertEqual(len(TestRuntimeContext.reports["chain_id_0"]), 2)
    self.assertFalse(TestRuntimeContext.reports["chain_id_0"][0].ok)
    self.assertTrue(TestRuntimeContext.reports["chain_id_0"][1].ok)
    self.assertIsNone(TestRuntimeContext.terminated_by)
    self.assertIsNone(TestRuntimeContext.terminated_at_chain_id)

class TestRoutineCommandReportsFailedChainEvaluatorNotRunningDoFailed(unittest.TestCase):
  def test_command_chain(self):
    command_a_report = _mock_report(report_ok=False, isRunning=False)
    command_b_report = _mock_report(report_ok=False, isRunning=None)
    command_a = _mock_command(command_a_report)
    command_b = _mock_command(command_b_report)
    steps = [Step(command_a).not_running_do(command_b)]
    TestRoutine = Routine(steps=steps, verbose=False)
    TestRuntimeContext: RuntimeContext = TestRoutine.run()

    self.assertEqual(len(TestRuntimeContext.reports["chain_id_0"]), 2)
    self.assertFalse(TestRuntimeContext.reports["chain_id_0"][0].ok)
    self.assertFalse(TestRuntimeContext.reports["chain_id_0"][1].ok)
    self.assertIsNone(TestRuntimeContext.terminated_by)
    self.assertIsNone(TestRuntimeContext.terminated_at_chain_id)

class TestRoutineCommandReportsSuccessIsRunningFalseChainEvaluatorNotRunningDo(unittest.TestCase):
  def test_command_chain(self):
    command_a_report = _mock_report(report_ok=True, isRunning=False)
    command_b_report = _mock_report(report_ok=True, isRunning=None)
    command_a = _mock_command(command_a_report)
    command_b = _mock_command(command_b_report)
    steps = [Step(command_a).not_running_do(command_b)]
    TestRoutine = Routine(steps=steps, verbose=False)
    TestRuntimeContext: RuntimeContext = TestRoutine.run()

    self.assertEqual(len(TestRuntimeContext.reports["chain_id_0"]), 2)
    self.assertTrue(TestRuntimeContext.reports["chain_id_0"][0].ok)
    self.assertTrue(TestRuntimeContext.reports["chain_id_0"][1].ok)
    self.assertIsNone(TestRuntimeContext.terminated_by)
    self.assertIsNone(TestRuntimeContext.terminated_at_chain_id)

class TestRoutineCommandReportsFailedChainEvaluatorOnFailureDo(unittest.TestCase):
  def test_command_chain(self):
    command_a_report = _mock_report(report_ok=False, isRunning=None)
    command_b_report = _mock_report(report_ok=True, isRunning=None)
    command_a = _mock_command(command_a_report)
    command_b = _mock_command(command_b_report)
    steps = [Step(command_a).on_failure_do(command_b)]
    TestRoutine = Routine(steps=steps, verbose=False)
    TestRuntimeContext: RuntimeContext = TestRoutine.run()

    self.assertEqual(len(TestRuntimeContext.reports["chain_id_0"]), 2)
    self.assertFalse(TestRuntimeContext.reports["chain_id_0"][0].ok)
    self.assertTrue(TestRuntimeContext.reports["chain_id_0"][1].ok)
    self.assertIsNone(TestRuntimeContext.terminated_by)
    self.assertIsNone(TestRuntimeContext.terminated_at_chain_id)

class TestRoutineChainEvaluatorActionAbortHaltsNewChain(unittest.TestCase):
  def test_command_chain(self):
    command_a_report = _mock_report(report_ok=False, isRunning=None)
    command_b_report = _mock_report(report_ok=True, isRunning=None)
    command_a = _mock_command(command_a_report)
    command_b = _mock_command(command_b_report)
    steps = [Step(command_a).on_failure_do(CommandAction.ABORT), Step(command_b)]
    TestRoutine = Routine(steps=steps, verbose=False)
    TestRuntimeContext: RuntimeContext = TestRoutine.run()

    command_a.assert_called_once()
    command_b.assert_not_called()
    self.assertEqual(len(TestRuntimeContext.reports["chain_id_0"]), 1)
    self.assertEqual(TestRuntimeContext.terminated_by, CommandAction.ABORT)
    self.assertEqual(TestRuntimeContext.terminated_at_chain_id, 0)

class TestRoutineMultipleCommandReportsSuccess(unittest.TestCase):
  def test_command_chain(self):
    command_a_report = _mock_report(report_ok=True, isRunning=None)
    command_b_report = _mock_report(report_ok=True, isRunning=None)
    command_c_report = _mock_report(report_ok=True, isRunning=None)
    command_a = _mock_command(command_a_report)
    command_b = _mock_command(command_b_report)
    command_c = _mock_command(command_c_report)
    steps = [Step(command_a), Step(command_b), Step(command_c)]
    TestRoutine = Routine(steps=steps, verbose=False)
    TestRuntimeContext: RuntimeContext = TestRoutine.run()

    command_a.assert_called_once()
    command_b.assert_called_once()
    command_c.assert_called_once()
    self.assertEqual(len(TestRuntimeContext.reports), 3)
    self.assertIsNone(TestRuntimeContext.terminated_by)
    self.assertIsNone(TestRuntimeContext.terminated_at_chain_id)

def _mock_report(report_ok: bool, isRunning: bool | None) -> Mock:
  report = Mock()
  report.ok = report_ok
  report.isRunning = isRunning
  return report

def _mock_command(report) -> Mock:
  command = Mock(return_value=report)
  return command  