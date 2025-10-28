# Test Coverage Matrix

## Summary
- **Total Tests**: 62
- **All Passing**: ✅ Yes
- **Coverage**: 21.22% (Target: 70%)
- **Status**: ⚠️ Needs significant expansion

## README Feature → Test Coverage Mapping

| Feature | Status | Test File | Coverage | Missing Tests |
|---------|--------|-----------|----------|--------------|
| 🎯 **Dual Platform Support** | ✅ Complete | test_multiplatform_integration.py | ~85% | - |
| 🎨 **WCAG-Compliant Themes** | ✅ Complete | test_themes.py | ~75% | Auto-detection edge cases |
| ⚠️ **4-Level Alert System** | ❌ Missing | - | **0%** | ALL alert functionality |
| 🔮 **ML-Based Predictions** | ❌ Missing | - | **0%** | P90 calculations, trend analysis |
| 💾 **Cached Token Tracking** | ✅ Complete | test_platforms.py | ~70% | - |
| 📊 **Advanced Analytics** | ⚠️ Partial | test_platforms.py | ~40% | Session tracking, time-based queries |
| 📈 **Multiple View Modes** | ❌ Missing | - | **0%** | Table views, compact view, limit views |
| 🚀 **Real-Time Monitoring** | ❌ Missing | - | **0%** | CLI, display controller, refresh cycle |
| 🎨 **UI Components** | ❌ Missing | - | **0%** | Progress bars integration, layouts |
| ⚙️ **Settings Management** | ❌ Missing | - | **0%** | Config loading, env vars |
| 🕐 **Time Utilities** | ❌ Missing | - | **0%** | Date parsing, timezone handling |
| 📊 **Visualizations** | ❌ Missing | - | **0%** | Charts, graphs, sparklines |
| 💰 **Pricing Calculator** | ⚠️ Partial | test_platforms.py | ~38% | Multi-model scenarios, discounts |

## Module Coverage Breakdown

### ✅ Well Covered (>60%)
- platforms/base.py: 100%
- platforms/codex.py: 63.77%
- platforms/claude.py: 67.16%
- core/models.py: 75.50%
- ui/progress_bars.py: 78.16%
- ui/themes.py: 71.18%
- data/api_client.py: 72.09%

### ⚠️ Partially Covered (20-60%)
- core/pricing.py: 37.66%
- core/plans.py: 39.53%

### ❌ Not Covered (0-20%)
- **cli/main.py: 0%** ← Entry point not tested!
- **core/alerts.py: 0%** ← Critical feature not tested!
- **core/p90_calculator.py: 0%** ← ML predictions not tested!
- **core/settings.py: 0%**
- ui/components.py: 0%
- ui/display.py: 0%
- ui/display_controller.py: 0%
- ui/layouts.py: 0%
- ui/table_views.py: 0%
- ui/session_display.py: 0%
- ui/theme_switcher.py: 10.13%
- ui/visualizations.py: 0%
- utils/time_utils.py: 0%
- platforms/claude_enhanced.py: 0%

## Test Creation Priorities

### 🔴 Critical (P0) - Core README Features
1. **Alert System Tests** (core/alerts.py)
   - [ ] Alert level calculations (INFO/WARNING/CRITICAL/DANGER)
   - [ ] Threshold detection
   - [ ] Alert message formatting
   - [ ] Alert history tracking

2. **ML Predictions Tests** (core/p90_calculator.py)
   - [ ] P90 percentile calculations
   - [ ] Trend analysis
   - [ ] Burn rate predictions
   - [ ] Usage forecasting

3. **CLI Integration Tests** (cli/main.py)
   - [ ] Argument parsing
   - [ ] Platform selection
   - [ ] Theme selection
   - [ ] View mode selection
   - [ ] Error handling

### 🟡 Important (P1) - UI Features
4. **View Modes Tests** (ui/table_views.py, ui/display.py)
   - [ ] Daily view rendering
   - [ ] Monthly view rendering
   - [ ] Compact view rendering
   - [ ] Limits view rendering

5. **Display Controller Tests** (ui/display_controller.py)
   - [ ] Real-time refresh
   - [ ] State updates
   - [ ] Dual-platform rendering

6. **Components Tests** (ui/components.py)
   - [ ] Panel creation
   - [ ] Progress bar rendering
   - [ ] Token usage display
   - [ ] Cost display

### 🟢 Nice to Have (P2) - Support Features
7. **Settings Tests** (core/settings.py)
   - [ ] Config file loading
   - [ ] Environment variable parsing
   - [ ] Default values

8. **Time Utilities Tests** (utils/time_utils.py)
   - [ ] Date parsing
   - [ ] Timezone conversions
   - [ ] Period calculations

9. **Visualizations Tests** (ui/visualizations.py)
   - [ ] Chart rendering
   - [ ] Sparkline generation
   - [ ] Graph layouts

## Test Files to Create

```
tests/
├── test_cli/
│   ├── test_main.py              # CLI entry point tests
│   ├── test_argument_parser.py   # Argument validation
│   └── test_integration.py       # End-to-end CLI tests
├── test_core/
│   ├── test_alerts.py            # Alert system tests
│   ├── test_p90_calculator.py    # ML prediction tests
│   ├── test_settings.py          # Settings management tests
│   └── test_pricing.py           # Enhanced pricing tests
├── test_ui/
│   ├── test_components.py        # UI component tests
│   ├── test_display.py           # Display rendering tests
│   ├── test_display_controller.py # Controller tests
│   ├── test_layouts.py           # Layout tests
│   ├── test_table_views.py       # Table view tests
│   ├── test_visualizations.py    # Visualization tests
│   └── test_theme_switcher.py    # Theme switching tests
└── test_utils/
    └── test_time_utils.py        # Time utility tests
```

## Coverage Goal

- **Current**: 21.22%
- **Target**: 70%
- **Gap**: 48.78%
- **Estimated Tests Needed**: ~150-200 additional test cases

## Next Steps

1. ✅ Create this test matrix
2. ⏳ Create priority test files (P0: Alerts, P90, CLI)
3. ⏳ Create UI test files (P1: Display, Views, Components)
4. ⏳ Create support test files (P2: Settings, Utils)
5. ⏳ Run full test suite and verify coverage reaches 70%+
6. ⏳ Update CI/CD to enforce coverage requirements
