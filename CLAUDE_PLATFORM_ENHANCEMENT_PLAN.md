# Claude Platform Enhancement Plan

## Overview
This document outlines the necessary enhancements to make ClaudePlatform feature-complete and compatible with claude-code-usage-monitor.

## Critical Issue: Data Source Incompatibility

### Current State
- ClaudePlatform writes to `~/.claude-monitor/usage_log.jsonl`
- Does not read Claude Code's native data files
- Acts as a write-only logger, not a usage monitor

### Required Change
- Must read from `~/.config/claude/projects/*.jsonl` (Claude Code's native files)
- OR from `~/.claude/projects/*.jsonl` (alternative location)
- Must parse Claude Code's JSONL format

## Missing Features Breakdown

### 1. Data Reading from Claude Code (CRITICAL)

**Current**: No reading of Claude's native files
**Required**: JSONL reader for Claude Code's data format

Key fields in Claude Code's JSONL format:
```json
{
  "timestamp": "2025-01-15T10:30:00.000Z",
  "message_id": "msg_123abc",
  "request_id": "req_456def",
  "model": "claude-sonnet-4-20250514",
  "input_tokens": 1000,
  "output_tokens": 500,
  "cache_creation_tokens": 2000,
  "cache_read_tokens": 5000,
  "cost": 0.045,
  "message": {
    "id": "msg_123abc",
    "type": "message",
    "role": "assistant",
    "content": [...],
    "usage": {
      "input_tokens": 1000,
      "output_tokens": 500,
      "cache_creation_input_tokens": 2000,
      "cache_read_input_tokens": 5000
    }
  }
}
```

### 2. Cache Token Tracking (CRITICAL)

**Current**: Single `cached_tokens` field (ambiguous)
**Required**: Separate tracking for cache_creation and cache_read

Pricing model:
- cache_creation_tokens: 1.25x input price (25% premium)
- cache_read_tokens: 0.1x input price (90% discount)

### 3. 5-Hour Session Blocks (HIGH PRIORITY)

**Current**: Simple SessionData with any duration
**Required**: SessionBlock with 5-hour rolling windows

Features:
- Round timestamps to hour boundaries
- 5-hour duration blocks
- Gap detection (inactivity periods)
- Active/inactive status
- Per-model statistics within block

### 4. Limit Detection (HIGH PRIORITY)

**Current**: No limit detection
**Required**: Parse system messages for limits

Types of limits:
- General token limits
- Opus-specific rate limits
- System limit messages
- Tool result limit messages

### 5. Plan Support (MEDIUM PRIORITY)

**Current**: No plan definitions
**Required**: Pro/Max5/Max20/Custom plans

```python
PLAN_LIMITS = {
    "pro": {"tokens": 44000, "cost": 18.00},
    "max5": {"tokens": 88000, "cost": 35.00},
    "max20": {"tokens": 220000, "cost": 140.00},
}
```

### 6. Additional Model Support (MEDIUM PRIORITY)

**Current**: Sonnet and Opus 3
**Required**: Add Haiku and Opus 4

```python
"claude-haiku": {
    "prompt": 0.25,
    "completion": 1.25,
    "cache_creation": 0.3125,  # 1.25x
    "cache_read": 0.025,       # 0.1x
},
"claude-opus-4-20250514": {
    "prompt": 15.00,
    "completion": 75.00,
    "cache_creation": 18.75,
    "cache_read": 1.50,
},
```

### 7. Time Window Support (MEDIUM PRIORITY)

**Current**: Only 24-hour window
**Required**: Configurable windows (24h, 168h, 192h, 720h)

For P90 analysis: 192 hours (8 days)
For weekly stats: 168 hours (7 days)
For monthly stats: 720 hours (30 days)

### 8. Configuration Persistence (LOW PRIORITY)

**Current**: No configuration persistence
**Required**: Save preferences to `~/.claude-monitor/last_used.json`

Settings to persist:
- View type (realtime/daily/monthly)
- Theme preference
- Timezone
- Time format
- Custom token limits
- Plan type (NOT persisted in original, must be specified each run)

### 9. Deduplication (LOW PRIORITY)

**Current**: No deduplication
**Required**: Deduplicate by message_id + request_id

Prevents double-counting when:
- Same entry appears in multiple files
- Re-reading files
- Processing overlapping data

### 10. Model Name Normalization (LOW PRIORITY)

**Current**: Basic model matching
**Required**: Comprehensive normalization

```python
def normalize_model_name(model: str) -> str:
    # Map variants to standard names
    # "claude-sonnet-4-20250514" → "claude-sonnet-4"
    # "Claude 3.5 Sonnet" → "claude-3-5-sonnet"
```

## Implementation Priority

### Phase 1: Critical Compatibility (Week 1)
1. Implement Claude Code JSONL reader
2. Change data source to ~/.config/claude/projects/
3. Add cache_creation_tokens and cache_read_tokens fields
4. Update cost calculation for cache tokens

### Phase 2: Core Features (Week 2)
1. Implement 5-hour SessionBlock model
2. Add gap detection
3. Add limit detection
4. Add plan support

### Phase 3: Additional Features (Week 3)
1. Add Haiku and Opus 4 models
2. Extend time window support
3. Add monthly aggregation
4. Implement configuration persistence

### Phase 4: Polish & Testing (Week 4)
1. Add deduplication
2. Improve model normalization
3. Comprehensive testing
4. Documentation

## Testing Requirements

### Unit Tests
- JSONL parsing with sample Claude Code data
- Cache token cost calculations
- Session block creation and gap detection
- Limit message detection
- Model normalization

### Integration Tests
- Read actual Claude Code data files
- Multi-session aggregation
- Time window queries
- Plan limit calculations

### Regression Tests
- Ensure backward compatibility with existing genai-code-usage-monitor
- Verify multi-platform state management
- Test platform switching

## Compatibility Considerations

### With Original claude-code-usage-monitor
- ClaudePlatform should read the SAME data files
- Cost calculations should match exactly
- Session blocks should align with 5-hour windows
- P90 logic should produce similar results

### With genai-code-usage-monitor
- Must not break CodexPlatform
- MultiPlatformState should handle both platforms
- Shared models (Alert, BurnRate, etc.) should work for both
- CLI should support platform selection

## Success Criteria

1. **Feature Parity**: 100% of claude-code-usage-monitor features implemented
2. **Data Compatibility**: Can read Claude Code's native JSONL files
3. **Cost Accuracy**: Cost calculations match claude-code-usage-monitor exactly
4. **Session Tracking**: 5-hour session blocks work correctly
5. **Cache Support**: Separate cache_creation and cache_read tracking
6. **Plan Support**: All plan types (Pro/Max5/Max20/Custom) supported
7. **Testing**: >90% code coverage with passing tests
8. **Documentation**: Comprehensive docs for all new features

## Risk Mitigation

### Risk: Breaking Existing Functionality
**Mitigation**: Comprehensive regression testing, feature flags for new features

### Risk: Data Source Changes in Claude Code
**Mitigation**: Environment variable for configurable data path, graceful fallback

### Risk: Performance with Large JSONL Files
**Mitigation**: Streaming parser, file caching, time-window filtering

### Risk: Timezone Handling
**Mitigation**: Use TimezoneHandler class, UTC normalization, timezone-aware datetime objects

## Next Steps

1. Review and approve this enhancement plan
2. Create detailed technical specifications for each feature
3. Set up development environment with sample Claude Code data
4. Begin Phase 1 implementation
5. Iterative development with continuous testing
