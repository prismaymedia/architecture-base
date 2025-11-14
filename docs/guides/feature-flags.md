# Feature Flags Guide

> **Purpose**: Enable continuous deployment while controlling feature rollout  
> **Status**: ✅ Active  
> **Last Updated**: 2025-11-14

Feature flags (also called feature toggles) allow you to deploy code with incomplete or risky features that can be toggled on/off without redeploying.

## Table of Contents

- [Why Feature Flags?](#why-feature-flags)
- [Types of Feature Flags](#types-of-feature-flags)
- [Implementation in Python](#implementation-in-python)
- [Implementation in React](#implementation-in-react)
- [Best Practices](#best-practices)
- [Flag Lifecycle](#flag-lifecycle)
- [Common Patterns](#common-patterns)
- [Troubleshooting](#troubleshooting)

## Why Feature Flags?

Feature flags enable:

- ✅ **Trunk-Based Development**: Merge incomplete features safely
- ✅ **Gradual Rollout**: Enable features for subset of users
- ✅ **A/B Testing**: Test different implementations
- ✅ **Kill Switch**: Disable problematic features instantly
- ✅ **Continuous Deployment**: Deploy anytime without risk
- ✅ **Decoupled Deployment**: Deploy code ≠ release feature

### Without Feature Flags

```python
# Can't merge until complete
# PR stays open for days/weeks
# Integration conflicts accumulate
# Risk of breaking production
```

### With Feature Flags

```python
# Merge incomplete code safely
if feature_flags.new_payment_flow_enabled:
    result = await new_payment_service.process(payment)
else:
    result = await legacy_payment_service.process(payment)

# Enable when ready, no deployment needed
```

## Types of Feature Flags

### 1. Release Flags (Short-term)

**Purpose**: Control rollout of new features  
**Lifetime**: Temporary (remove after rollout complete)  
**Audience**: All users or percentage-based

```python
# Enable new order validation for 10% of users
if feature_flags.is_enabled("new_order_validation", user_id):
    await new_validation_service.validate(order)
else:
    await legacy_validation_service.validate(order)
```

**Remove after 100% rollout.**

### 2. Ops Flags (Long-term)

**Purpose**: Operational control (circuit breakers, rate limiting)  
**Lifetime**: Permanent  
**Audience**: System-level

```python
# Circuit breaker for external payment gateway
if feature_flags.payment_gateway_enabled:
    result = await external_gateway.process(payment)
else:
    result = await fallback_processor.process(payment)
```

**Keep indefinitely for operational control.**

### 3. Experiment Flags (Short-term)

**Purpose**: A/B testing, experiments  
**Lifetime**: Duration of experiment  
**Audience**: Specific user segments

```python
# A/B test: two different checkout flows
variant = feature_flags.get_variant("checkout_flow_experiment", user_id)
if variant == "variant_a":
    return await checkout_flow_a(cart)
elif variant == "variant_b":
    return await checkout_flow_b(cart)
else:
    return await default_checkout(cart)
```

**Remove after experiment concludes.**

### 4. Permission Flags (Long-term)

**Purpose**: User/role-based access control  
**Lifetime**: Permanent or long-term  
**Audience**: Specific users/roles

```python
# Premium feature only for paid users
if feature_flags.has_permission(user_id, "advanced_analytics"):
    return await analytics_service.get_advanced_report(user_id)
else:
    return await analytics_service.get_basic_report(user_id)
```

## Implementation in Python

### Basic Implementation

**1. Configuration (`app/core/config.py`):**

```python
from pydantic_settings import BaseSettings
from typing import Dict

class Settings(BaseSettings):
    # Feature flags
    FEATURE_NEW_PAYMENT_FLOW: bool = False
    FEATURE_ADVANCED_INVENTORY: bool = False
    FEATURE_EMAIL_NOTIFICATIONS: bool = True
    
    # Percentage rollouts (0-100)
    FEATURE_NEW_CHECKOUT_PERCENTAGE: int = 0
    
    class Config:
        env_file = ".env"

settings = Settings()
```

**2. Feature Flag Service (`app/core/feature_flags.py`):**

```python
import hashlib
from typing import Optional
from app.core.config import settings

class FeatureFlags:
    """Centralized feature flag management."""
    
    @staticmethod
    def is_enabled(flag_name: str, user_id: Optional[str] = None) -> bool:
        """
        Check if feature flag is enabled.
        
        Args:
            flag_name: Name of the feature flag
            user_id: Optional user ID for percentage rollouts
            
        Returns:
            True if feature is enabled for this user
        """
        # Simple boolean flags
        env_var = f"FEATURE_{flag_name.upper()}"
        if hasattr(settings, env_var):
            enabled = getattr(settings, env_var)
            if isinstance(enabled, bool):
                return enabled
        
        # Percentage-based rollout
        percentage_var = f"FEATURE_{flag_name.upper()}_PERCENTAGE"
        if hasattr(settings, percentage_var):
            percentage = getattr(settings, percentage_var)
            if user_id and percentage > 0:
                return FeatureFlags._is_in_percentage(user_id, percentage)
        
        return False
    
    @staticmethod
    def _is_in_percentage(user_id: str, percentage: int) -> bool:
        """Consistent hash-based percentage rollout."""
        if percentage >= 100:
            return True
        if percentage <= 0:
            return False
            
        # Consistent hash: same user_id always gets same result
        hash_value = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
        return (hash_value % 100) < percentage

# Global instance
feature_flags = FeatureFlags()
```

**3. Usage in Service Layer:**

```python
from app.core.feature_flags import feature_flags
from app.domain.services.payment_service import PaymentService, NewPaymentService

class OrderService:
    def __init__(
        self,
        payment_service: PaymentService,
        new_payment_service: NewPaymentService
    ):
        self.payment_service = payment_service
        self.new_payment_service = new_payment_service
    
    async def create_order(self, order_data: OrderCreate, user_id: str):
        """Create order with feature-flagged payment processing."""
        
        # Create order
        order = await self.order_repository.create(order_data)
        
        # Feature-flagged payment processing
        if feature_flags.is_enabled("new_payment_flow", user_id):
            payment_result = await self.new_payment_service.process(
                order.payment_info
            )
        else:
            payment_result = await self.payment_service.process(
                order.payment_info
            )
        
        # Update order with payment result
        order.payment_status = payment_result.status
        await self.order_repository.update(order)
        
        return order
```

**4. Environment Configuration (`.env`):**

```bash
# Feature flags - Boolean
FEATURE_NEW_PAYMENT_FLOW=false
FEATURE_ADVANCED_INVENTORY=true
FEATURE_EMAIL_NOTIFICATIONS=true

# Feature flags - Percentage rollout (0-100)
FEATURE_NEW_CHECKOUT_PERCENTAGE=10  # 10% of users

# Production environment flags
FEATURE_EXPERIMENTAL_SEARCH=false
FEATURE_PAYMENT_RETRY=true
```

### Advanced Implementation with LaunchDarkly/Unleash

For production systems, consider dedicated feature flag services:

```python
from ldclient import Context, LDClient

class FeatureFlagService:
    def __init__(self, sdk_key: str):
        self.client = LDClient(sdk_key)
    
    def is_enabled(self, flag_name: str, user_id: str, default: bool = False) -> bool:
        context = Context.builder(user_id).build()
        return self.client.variation(flag_name, context, default)
    
    def get_variant(self, flag_name: str, user_id: str) -> str:
        context = Context.builder(user_id).build()
        return self.client.variation(flag_name, context, "control")
```

## Implementation in React

### Basic Implementation

**1. Feature Flag Context (`src/contexts/FeatureFlagContext.tsx`):**

```typescript
import React, { createContext, useContext, ReactNode } from 'react';

interface FeatureFlags {
  newCheckoutFlow: boolean;
  advancedSearch: boolean;
  darkMode: boolean;
}

interface FeatureFlagContextType {
  flags: FeatureFlags;
  isEnabled: (flagName: keyof FeatureFlags) => boolean;
}

const FeatureFlagContext = createContext<FeatureFlagContextType | undefined>(
  undefined
);

export const FeatureFlagProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  // Load from environment variables or API
  const flags: FeatureFlags = {
    newCheckoutFlow: import.meta.env.VITE_FEATURE_NEW_CHECKOUT === 'true',
    advancedSearch: import.meta.env.VITE_FEATURE_ADVANCED_SEARCH === 'true',
    darkMode: import.meta.env.VITE_FEATURE_DARK_MODE === 'true',
  };

  const isEnabled = (flagName: keyof FeatureFlags): boolean => {
    return flags[flagName] ?? false;
  };

  return (
    <FeatureFlagContext.Provider value={{ flags, isEnabled }}>
      {children}
    </FeatureFlagContext.Provider>
  );
};

export const useFeatureFlags = () => {
  const context = useContext(FeatureFlagContext);
  if (!context) {
    throw new Error('useFeatureFlags must be used within FeatureFlagProvider');
  }
  return context;
};
```

**2. Usage in Components:**

```typescript
import { useFeatureFlags } from '@/contexts/FeatureFlagContext';

export const CheckoutPage = () => {
  const { isEnabled } = useFeatureFlags();

  return (
    <div>
      {isEnabled('newCheckoutFlow') ? (
        <NewCheckoutFlow />
      ) : (
        <LegacyCheckoutFlow />
      )}
    </div>
  );
};
```

**3. Feature Flag Component:**

```typescript
import { useFeatureFlags } from '@/contexts/FeatureFlagContext';

interface FeatureProps {
  flag: string;
  children: ReactNode;
  fallback?: ReactNode;
}

export const Feature: React.FC<FeatureProps> = ({ 
  flag, 
  children, 
  fallback = null 
}) => {
  const { isEnabled } = useFeatureFlags();
  
  return isEnabled(flag) ? <>{children}</> : <>{fallback}</>;
};

// Usage
<Feature flag="newCheckoutFlow">
  <NewCheckoutFlow />
</Feature>
```

**4. Environment Variables (`.env.local`):**

```bash
VITE_FEATURE_NEW_CHECKOUT=false
VITE_FEATURE_ADVANCED_SEARCH=true
VITE_FEATURE_DARK_MODE=true
```

## Best Practices

### 1. Naming Conventions

**Good:**
```python
FEATURE_NEW_PAYMENT_FLOW
FEATURE_ADVANCED_INVENTORY_TRACKING
FEATURE_EMAIL_NOTIFICATIONS_ENABLED
```

**Bad:**
```python
NEW_FEATURE  # Too vague
PAYMENT  # Unclear what it controls
FLAG_1  # Not descriptive
```

**Convention:**
- Prefix: `FEATURE_`
- Descriptive name: What feature it controls
- Uppercase with underscores
- Boolean or percentage suffix if needed

### 2. Flag Lifecycle Management

**Track flags in documentation:**

```markdown
# docs/feature-flags.md

| Flag Name | Type | Status | Created | Target Removal | Owner |
|-----------|------|--------|---------|----------------|-------|
| NEW_PAYMENT_FLOW | Release | Active | 2025-11-01 | 2025-12-01 | Team Payments |
| PAYMENT_GATEWAY_CIRCUIT_BREAKER | Ops | Permanent | 2025-10-15 | N/A | Team Platform |
| CHECKOUT_AB_TEST | Experiment | Active | 2025-11-10 | 2025-11-24 | Team Frontend |
```

**Set removal reminders:**
- Release flags: Remove after 100% rollout (typically 2-4 weeks)
- Experiment flags: Remove after experiment ends
- Technical debt: Create tasks to clean up old flags

### 3. Default to Safe State

```python
# Default to old/safe behavior if flag fails
if feature_flags.is_enabled("risky_new_feature", user_id):
    try:
        return await new_risky_implementation()
    except Exception as e:
        logger.error(f"New feature failed, falling back: {e}")
        return await legacy_implementation()
else:
    return await legacy_implementation()
```

### 4. Keep Logic Simple

**Bad:**
```python
# Complex nested flags
if feature_flags.is_enabled("feature_a"):
    if feature_flags.is_enabled("feature_b"):
        if feature_flags.is_enabled("feature_c"):
            # Too complex!
```

**Good:**
```python
# Simple, clear logic
if feature_flags.is_enabled("new_payment_flow"):
    return await new_payment_service.process(payment)
else:
    return await legacy_payment_service.process(payment)
```

### 5. Test Both Paths

```python
# Unit tests for both enabled and disabled states
class TestOrderService:
    async def test_create_order_new_payment_flow_enabled(self, mocker):
        """Test with new payment flow enabled."""
        mocker.patch('app.core.feature_flags.feature_flags.is_enabled', return_value=True)
        # ... test new flow
    
    async def test_create_order_new_payment_flow_disabled(self, mocker):
        """Test with new payment flow disabled."""
        mocker.patch('app.core.feature_flags.feature_flags.is_enabled', return_value=False)
        # ... test old flow
```

### 6. Monitor Flag Usage

```python
from app.core.monitoring import metrics

async def create_order(order_data: OrderCreate, user_id: str):
    is_new_flow = feature_flags.is_enabled("new_payment_flow", user_id)
    
    # Track which flow is used
    metrics.increment(
        "payment_flow_usage",
        tags={"flow": "new" if is_new_flow else "legacy"}
    )
    
    if is_new_flow:
        return await new_payment_service.process(order_data.payment)
    else:
        return await legacy_payment_service.process(order_data.payment)
```

### 7. Document Flags

Add comments explaining the flag:

```python
# FEATURE_NEW_PAYMENT_FLOW
# Enable new Stripe-based payment processing with retry logic.
# Rollout plan: 10% -> 50% -> 100% over 2 weeks
# Owner: Team Payments
# Target removal: 2025-12-01
# Ticket: TASK-042
if feature_flags.is_enabled("new_payment_flow", user_id):
    # New implementation
```

## Flag Lifecycle

### Phase 1: Introduction (0% - Testing)

```bash
# .env
FEATURE_NEW_PAYMENT_FLOW=false
FEATURE_NEW_PAYMENT_FLOW_PERCENTAGE=0
```

- Deploy to production with flag OFF
- Test manually with flag ON in staging
- Verify both code paths work
- Monitor for errors

### Phase 2: Canary (1-10% - Early Validation)

```bash
# .env - Week 1
FEATURE_NEW_PAYMENT_FLOW_PERCENTAGE=1  # 1% of users

# Monitor for 24-48 hours
# If stable, increase

# .env - Week 1, Day 3
FEATURE_NEW_PAYMENT_FLOW_PERCENTAGE=5

# .env - Week 1, Day 5
FEATURE_NEW_PAYMENT_FLOW_PERCENTAGE=10
```

- Enable for small percentage
- Monitor metrics closely
- Be ready to disable instantly
- Gather initial feedback

### Phase 3: Gradual Rollout (10-100%)

```bash
# .env - Week 2
FEATURE_NEW_PAYMENT_FLOW_PERCENTAGE=25

# .env - Week 2, Day 4
FEATURE_NEW_PAYMENT_FLOW_PERCENTAGE=50

# .env - Week 3
FEATURE_NEW_PAYMENT_FLOW_PERCENTAGE=75

# .env - Week 3, Day 4
FEATURE_NEW_PAYMENT_FLOW_PERCENTAGE=100
```

- Increase percentage gradually
- Monitor key metrics
- Address issues before increasing
- Communicate with stakeholders

### Phase 4: Full Rollout (100%)

```bash
# .env - Week 4
FEATURE_NEW_PAYMENT_FLOW=true  # Simplify to boolean
# Remove percentage-based logic from code
```

- All users on new feature
- Monitor for 1-2 weeks
- Prepare for cleanup

### Phase 5: Cleanup (Remove Flag)

```python
# Before cleanup:
if feature_flags.is_enabled("new_payment_flow", user_id):
    return await new_payment_service.process(payment)
else:
    return await legacy_payment_service.process(payment)

# After cleanup:
return await payment_service.process(payment)  # New is now default
# Delete legacy_payment_service.py
```

- Remove flag checks from code
- Delete old/legacy implementation
- Remove flag from configuration
- Update tests
- Deploy cleanup

## Common Patterns

### Pattern 1: Gradual Rollout

```python
# Start at 0%, increase gradually
percentage = settings.FEATURE_NEW_CHECKOUT_PERCENTAGE
if feature_flags.is_enabled("new_checkout", user_id):
    # New implementation
else:
    # Old implementation
```

### Pattern 2: Kill Switch

```python
# Disable problematic feature instantly
if not feature_flags.is_enabled("external_api_integration"):
    logger.warning("External API integration disabled via feature flag")
    return await fallback_handler()

try:
    return await external_api.call()
except Exception as e:
    logger.error(f"External API failed: {e}")
    # Disable via flag in .env without redeploying
    return await fallback_handler()
```

### Pattern 3: A/B Testing

```python
# Serve different variants to different users
variant = feature_flags.get_variant("pricing_page_test", user_id)
if variant == "variant_a":
    return await render_pricing_page_a()
elif variant == "variant_b":
    return await render_pricing_page_b()
else:
    return await render_pricing_page_default()
```

### Pattern 4: Permission-Based

```python
# Feature available only to premium users
if feature_flags.has_permission(user_id, "advanced_analytics"):
    return await analytics_service.get_advanced_metrics(user_id)
else:
    raise PermissionError("Advanced analytics requires premium subscription")
```

### Pattern 5: Environment-Specific

```python
# Enable in staging, disable in production
if settings.ENVIRONMENT == "staging":
    feature_flags.override("experimental_feature", True)
```

## Troubleshooting

### Issue 1: Flag Not Taking Effect

**Problem:** Changed flag but behavior unchanged

**Solutions:**
1. Check environment variable loaded: `echo $FEATURE_NAME`
2. Restart service to reload config
3. Clear cache if caching feature flag values
4. Verify flag name matches exactly (case-sensitive)
5. Check feature flag service logs

### Issue 2: Inconsistent Behavior

**Problem:** Feature sometimes enabled, sometimes not

**Solutions:**
1. Verify hash-based rollout is deterministic
2. Check if flag value changes between requests
3. Ensure same user_id used throughout request
4. Verify configuration not overridden somewhere

### Issue 3: Can't Remove Flag

**Problem:** Flag still referenced in code

**Solutions:**
1. Search codebase: `grep -r "FEATURE_NAME"`
2. Check all microservices
3. Remove from tests
4. Update documentation
5. Create checklist for flag removal

## Related Documentation

- [Version Control Workflow](version-control-workflow.md)
- [ADR-007: Trunk-Based Development](../adr/007-trunk-based-development.md)
- [CI/CD Pipeline Guide](cicd-pipeline.md)

---

**Questions?** Contact the Platform Team on Slack #platform channel.
