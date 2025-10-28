# CLI Test Suite Coverage Summary

## Overview
Comprehensive test suite for `/Users/bytedance/genai-code-usage-monitor/src/genai_code_usage_monitor/cli/main.py`

**File:** `/Users/bytedance/genai-code-usage-monitor/tests/test_cli/test_main.py`

## Test Statistics

- **Total Test Classes:** 12
- **Total Test Methods:** 80
- **Total Fixtures:** 7
- **Expected Coverage:** >85% of cli/main.py

## Test Coverage Categories

### 1. Argument Parser Tests (TestArgumentParser - 29 tests)

Tests the `create_parser()` function and argument parsing logic:

#### Default Values (1 test)
- ✓ `test_default_values` - Verifies all CLI arguments have correct defaults

#### Platform Selection (3 tests)
- ✓ `test_platform_choices_valid` - Tests valid platforms: codex, claude, all
- ✓ `test_platform_invalid_choice` - Tests invalid platform raises error
- ✓ `test_parser_creation` - Tests parser is created successfully

#### Plan Selection (2 tests)
- ✓ `test_plan_choices_valid` - Tests all plan types from PLANS dict
- ✓ `test_plan_invalid_choice` - Tests invalid plan raises error

#### View Mode Selection (2 tests)
- ✓ `test_view_mode_choices_valid` - Tests all view modes: realtime, daily, monthly, compact, limits
- ✓ `test_view_mode_invalid_choice` - Tests invalid view mode raises error

#### Theme Selection (2 tests)
- ✓ `test_theme_choices_valid` - Tests all themes: auto, light, dark, classic
- ✓ `test_theme_invalid_choice` - Tests invalid theme raises error

#### Custom Limits (4 tests)
- ✓ `test_custom_limit_tokens` - Tests token limit argument parsing
- ✓ `test_custom_limit_tokens_invalid` - Tests invalid token limit
- ✓ `test_custom_limit_cost` - Tests cost limit argument parsing
- ✓ `test_custom_limit_cost_invalid` - Tests invalid cost limit

#### Time Options (5 tests)
- ✓ `test_timezone_argument` - Tests timezone argument (auto/custom)
- ✓ `test_time_format_choices` - Tests time format: auto, 12h, 24h
- ✓ `test_time_format_invalid` - Tests invalid time format
- ✓ `test_reset_hour_valid` - Tests valid reset hour values (0-23)
- ✓ `test_reset_hour_invalid` - Tests invalid reset hour

#### Refresh Rate Options (2 tests)
- ✓ `test_refresh_rate_argument` - Tests refresh rate argument
- ✓ `test_refresh_per_second_argument` - Tests refresh per second argument

#### Logging Options (4 tests)
- ✓ `test_log_level_choices` - Tests all log levels
- ✓ `test_log_level_invalid` - Tests invalid log level
- ✓ `test_log_file_argument` - Tests log file path argument
- ✓ `test_debug_flag` - Tests debug flag

#### Other Options (3 tests)
- ✓ `test_clear_flag` - Tests clear configuration flag
- ✓ `test_version_flag` - Tests --version flag
- ✓ `test_version_flag_short` - Tests -v flag
- ✓ `test_combined_arguments` - Tests multiple arguments together

### 2. Platform Selection Tests (TestPlatformSelection - 6 tests)

Tests platform initialization logic in `run_monitor()`:

- ✓ `test_platform_codex_only` - Verifies only CodexPlatform is created for --platform=codex
- ✓ `test_platform_claude_only` - Verifies only ClaudePlatform is created for --platform=claude
- ✓ `test_platform_all_creates_both` - Verifies both platforms created for --platform=all
- ✓ `test_platform_default_is_all` - Verifies default platform is 'all'
- ✓ `test_platform_single_uses_display_live` - Verifies single platform uses display_live()
- ✓ `test_platform_multi_uses_multiplatform_display` - Verifies multi-platform uses display_live_multiplatform()

### 3. Plan Integration Tests (TestPlanIntegration - 7 tests)

Tests PlanManager initialization and custom limits:

- ✓ `test_plan_manager_initialized_with_plan` - Verifies PlanManager initialized with selected plan
- ✓ `test_each_plan_type` - Tests each plan type from PLANS dict
- ✓ `test_custom_plan_default` - Verifies custom is default plan
- ✓ `test_custom_limit_tokens_applied` - Verifies custom token limit is applied
- ✓ `test_custom_limit_cost_applied` - Verifies custom cost limit is applied
- ✓ `test_custom_limits_both_applied` - Verifies both limits applied together
- ✓ `test_custom_limits_without_custom_plan` - Verifies limits work with any plan

### 4. View Mode Tests (TestViewModes - 6 tests)

Tests view mode configuration:

- ✓ `test_view_mode_realtime` - Tests realtime view mode
- ✓ `test_view_mode_daily` - Tests daily view mode
- ✓ `test_view_mode_monthly` - Tests monthly view mode
- ✓ `test_view_mode_compact` - Tests compact view mode
- ✓ `test_view_mode_limits` - Tests limits view mode
- ✓ `test_view_mode_default_is_realtime` - Verifies default is realtime

### 5. Theme Selection Tests (TestThemeSelection - 5 tests)

Tests theme configuration:

- ✓ `test_theme_auto` - Tests auto theme
- ✓ `test_theme_light` - Tests light theme
- ✓ `test_theme_dark` - Tests dark theme
- ✓ `test_theme_classic` - Tests classic theme
- ✓ `test_theme_default_is_auto` - Verifies default is auto

### 6. Settings Integration Tests (TestSettingsIntegration - 2 tests)

Tests Settings object initialization:

- ✓ `test_settings_initialized_with_all_args` - Verifies all CLI args passed to Settings
- ✓ `test_settings_default_values` - Verifies default values passed to Settings

### 7. Error Handling Tests (TestErrorHandling - 5 tests)

Tests error handling scenarios:

- ✓ `test_platform_initialization_error` - Tests platform initialization failure
- ✓ `test_platform_initialization_error_with_debug` - Tests error with debug mode
- ✓ `test_unexpected_error_during_monitoring` - Tests unexpected error during monitoring
- ✓ `test_keyboard_interrupt_handling` - Tests graceful Ctrl+C handling
- ✓ `test_keyboard_interrupt_multiplatform` - Tests Ctrl+C with multiple platforms

### 8. Main Function Tests (TestMainFunction - 5 tests)

Tests `main()` entry point:

- ✓ `test_main_calls_run_monitor` - Verifies main() calls run_monitor()
- ✓ `test_main_clear_flag` - Tests --clear flag deletes config
- ✓ `test_main_clear_flag_no_config` - Tests --clear when no config exists
- ✓ `test_main_version_flag` - Tests --version displays version
- ✓ `test_main_with_all_arguments` - Tests main() with comprehensive arguments

### 9. Refresh Rate Configuration Tests (TestRefreshRateConfiguration - 3 tests)

Tests refresh rate configuration:

- ✓ `test_refresh_rate_passed_to_controller` - Verifies refresh rate passed to DisplayController
- ✓ `test_refresh_per_second_passed_to_settings` - Verifies refresh per second passed to Settings
- ✓ `test_default_refresh_values` - Verifies default refresh values

### 10. Startup Messages Tests (TestStartupMessages - 4 tests)

Tests startup info display:

- ✓ `test_version_displayed_on_startup` - Verifies version shown on startup
- ✓ `test_platform_info_displayed` - Verifies platform info shown
- ✓ `test_plan_info_displayed` - Verifies plan info shown
- ✓ `test_exit_message_displayed` - Verifies exit message shown

### 11. Component Integration Tests (TestComponentIntegration - 4 tests)

Tests integration with other components:

- ✓ `test_usage_tracker_initialized_with_config_dir` - Verifies UsageTracker initialization
- ✓ `test_display_controller_receives_correct_params` - Verifies DisplayController params
- ✓ `test_single_platform_passes_correct_args_to_display` - Verifies single platform args
- ✓ `test_multi_platform_passes_correct_args_to_display` - Verifies multi-platform args

### 12. End-to-End Scenario Tests (TestEndToEndScenarios - 4 tests)

Tests complete workflows:

- ✓ `test_typical_codex_monitoring_scenario` - Tests typical Codex-only monitoring
- ✓ `test_typical_multi_platform_scenario` - Tests typical multi-platform monitoring
- ✓ `test_development_debug_scenario` - Tests development with debug enabled
- ✓ `test_custom_plan_full_configuration` - Tests custom plan with full config

## Fixtures

All tests use mocking to avoid real API calls or UI initialization:

1. **mock_settings** - Mocks Settings class
2. **mock_plan_manager** - Mocks PlanManager class
3. **mock_codex_platform** - Mocks CodexPlatform class
4. **mock_claude_platform** - Mocks ClaudePlatform class
5. **mock_usage_tracker** - Mocks UsageTracker class
6. **mock_display_controller** - Mocks DisplayController class
7. **all_mocks** - Convenience fixture combining all mocks

## What's Tested

### Core Functions
- ✓ `create_parser()` - Argument parser creation and configuration
- ✓ `run_monitor()` - Monitor initialization and execution
- ✓ `main()` - Main entry point logic

### Argument Parsing
- ✓ All argument choices and validations
- ✓ Default values
- ✓ Invalid input handling
- ✓ Combined arguments

### Platform Management
- ✓ Platform selection logic
- ✓ Single vs multi-platform modes
- ✓ Platform initialization

### Plan Management
- ✓ Plan selection
- ✓ Custom limits application
- ✓ Plan manager initialization

### Configuration
- ✓ Settings initialization
- ✓ View modes
- ✓ Themes
- ✓ Refresh rates
- ✓ Time settings
- ✓ Logging settings

### Error Handling
- ✓ Platform initialization errors
- ✓ Keyboard interrupt (Ctrl+C)
- ✓ Unexpected errors
- ✓ Debug mode error reporting

### User Feedback
- ✓ Startup messages
- ✓ Version display
- ✓ Platform info
- ✓ Plan info
- ✓ Exit messages

## What's NOT Tested (By Design)

These are intentionally NOT tested as they require integration testing:

- ❌ Real API calls to OpenAI/Anthropic
- ❌ Actual UI rendering and display
- ❌ Real-time data fetching
- ❌ File system operations (beyond mocking)
- ❌ Live console output
- ❌ Interactive terminal features

## Running the Tests

```bash
# Run all CLI tests
pytest tests/test_cli/test_main.py -v

# Run specific test class
pytest tests/test_cli/test_main.py::TestArgumentParser -v

# Run specific test
pytest tests/test_cli/test_main.py::TestArgumentParser::test_default_values -v

# Run with coverage
pytest tests/test_cli/test_main.py --cov=genai_code_usage_monitor.cli.main --cov-report=html

# Run with coverage and show missing lines
pytest tests/test_cli/test_main.py --cov=genai_code_usage_monitor.cli.main --cov-report=term-missing
```

## Expected Coverage

Based on the comprehensive test suite:

- **Argument Parser:** ~95% coverage
- **run_monitor() function:** ~90% coverage
- **main() function:** ~85% coverage
- **Overall cli/main.py:** >85% coverage

## Test Principles

1. **Unit Testing:** All tests are isolated unit tests, not integration tests
2. **Mocking:** Extensive use of mocking to avoid external dependencies
3. **Fast Execution:** Tests run quickly without real API calls or UI
4. **Comprehensive:** Cover all code paths, edge cases, and error scenarios
5. **Maintainable:** Clear test names and organization
6. **Independent:** Tests can run in any order

## Adding New Tests

When adding new CLI features, add tests for:

1. New argument parsing (add to TestArgumentParser)
2. New platform logic (add to TestPlatformSelection)
3. New plan features (add to TestPlanIntegration)
4. New error cases (add to TestErrorHandling)
5. New integration scenarios (add to TestEndToEndScenarios)

## Notes

- All tests use `unittest.mock` for mocking
- Tests validate both success and failure paths
- Error messages are validated where appropriate
- Version flag tests verify correct exit codes
- Keyboard interrupt tests ensure graceful shutdown
