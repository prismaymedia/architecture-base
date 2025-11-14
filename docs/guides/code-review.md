# Code Review Guidelines

> **Purpose**: Ensure code quality and knowledge sharing through effective reviews  
> **Status**: ✅ Active  
> **Last Updated**: 2025-11-14

This guide defines standards and best practices for code reviews in our microservices architecture.

## Table of Contents

- [Why Code Review?](#why-code-review)
- [Review Process](#review-process)
- [What to Review](#what-to-review)
- [Review Checklist](#review-checklist)
- [Providing Feedback](#providing-feedback)
- [Responding to Feedback](#responding-to-feedback)
- [Common Issues](#common-issues)
- [Best Practices](#best-practices)

## Why Code Review?

Code reviews provide multiple benefits:

- ✅ **Quality**: Catch bugs and issues before production
- ✅ **Knowledge Sharing**: Spread understanding across team
- ✅ **Consistency**: Maintain coding standards
- ✅ **Mentorship**: Learn from each other
- ✅ **Architecture**: Ensure alignment with design
- ✅ **Security**: Identify vulnerabilities early
- ✅ **Documentation**: Improve code clarity

## Review Process

### Timeline

- **Target**: 4 hours during business hours
- **Maximum**: 24 hours
- **Hotfix**: 1 hour

### Requirements for Merge

1. ✅ At least 1 approval (2 for critical changes)
2. ✅ All CI/CD checks passing
3. ✅ No unresolved conversations
4. ✅ PR description complete
5. ✅ Tests passing with adequate coverage

### Reviewer Responsibilities

- Review within target timeframe
- Provide constructive feedback
- Approve or request changes clearly
- Ask questions when unclear
- Verify tests and documentation

### Author Responsibilities

- Self-review before requesting review
- Respond to feedback within 24 hours
- Make requested changes promptly
- Mark conversations resolved when addressed
- Keep PR scope focused

## What to Review

### 1. Code Quality ⭐⭐⭐

**Check for:**

✅ **Readability**
- Variable/function names are clear and descriptive
- Code is self-documenting
- Complex logic has comments
- Consistent formatting

✅ **Maintainability**
- Functions are small and focused
- DRY principle applied (no duplication)
- SOLID principles followed
- Low coupling, high cohesion

✅ **Error Handling**
- Exceptions handled appropriately
- Error messages are clear
- No silent failures
- Proper logging on errors

**Example - Good:**

```python
async def process_payment(payment_data: PaymentData) -> PaymentResult:
    """
    Process payment using configured payment gateway.
    
    Args:
        payment_data: Payment information including amount and method
        
    Returns:
        PaymentResult with status and transaction ID
        
    Raises:
        PaymentValidationError: If payment data is invalid
        PaymentGatewayError: If payment processing fails
    """
    try:
        # Validate payment data
        await self._validate_payment(payment_data)
        
        # Process with gateway
        result = await self.gateway.charge(
            amount=payment_data.amount,
            method=payment_data.method
        )
        
        logger.info(
            "Payment processed successfully",
            transaction_id=result.transaction_id,
            amount=payment_data.amount
        )
        
        return result
        
    except ValidationError as e:
        logger.error("Payment validation failed", error=str(e))
        raise PaymentValidationError(f"Invalid payment data: {e}")
    except GatewayError as e:
        logger.error("Payment gateway error", error=str(e))
        raise PaymentGatewayError(f"Payment processing failed: {e}")
```

**Example - Bad:**

```python
# Poor naming, no error handling, no logging
async def process(d):
    r = await gw.charge(d.a, d.m)
    return r
```

### 2. Architecture & Design ⭐⭐⭐

**Check for:**

✅ **Architectural Patterns**
- Follows Clean Architecture layers
- Proper separation of concerns
- Domain logic isolated from infrastructure
- Dependency injection used correctly

✅ **Event-Driven Patterns**
- Event schemas follow standards
- Events are idempotent
- Correlation IDs included
- Versioning strategy followed

✅ **Database Design**
- Migrations included for schema changes
- Indexes on frequently queried columns
- No N+1 query patterns
- Transactions used appropriately

**Red Flags:**
- ❌ Direct database access from controllers
- ❌ Business logic in API layer
- ❌ Circular dependencies
- ❌ Tight coupling between services

### 3. Testing ⭐⭐⭐

**Check for:**

✅ **Test Coverage**
- New code has tests (>80% coverage)
- Edge cases covered
- Error paths tested
- Integration tests for complex flows

✅ **Test Quality**
- Tests are focused and clear
- Good test names (describe what's tested)
- Proper setup/teardown
- No flaky tests

✅ **Test Types**
- Unit tests for business logic
- Integration tests for APIs
- Contract tests for events
- Performance tests if applicable

**Example - Good Test:**

```python
class TestPaymentService:
    """Tests for payment processing service."""
    
    async def test_successful_payment_creates_transaction(
        self,
        payment_service,
        mock_gateway,
        sample_payment_data
    ):
        """
        Given a valid payment request
        When processing payment
        Then transaction is created and payment succeeds
        """
        # Arrange
        mock_gateway.charge.return_value = PaymentResult(
            status="success",
            transaction_id="txn_123"
        )
        
        # Act
        result = await payment_service.process_payment(sample_payment_data)
        
        # Assert
        assert result.status == "success"
        assert result.transaction_id == "txn_123"
        mock_gateway.charge.assert_called_once_with(
            amount=sample_payment_data.amount,
            method=sample_payment_data.method
        )
    
    async def test_payment_validation_error_raises_exception(
        self,
        payment_service
    ):
        """
        Given invalid payment data
        When processing payment
        Then PaymentValidationError is raised
        """
        # Arrange
        invalid_data = PaymentData(amount=-100)  # Negative amount
        
        # Act & Assert
        with pytest.raises(PaymentValidationError):
            await payment_service.process_payment(invalid_data)
```

### 4. Security ⭐⭐⭐

**Check for:**

✅ **Input Validation**
- All user input validated
- Parameterized queries (no SQL injection)
- Output encoding (no XSS)
- Rate limiting on APIs

✅ **Authentication & Authorization**
- Endpoints properly protected
- Permissions checked
- Tokens validated
- Session management secure

✅ **Secrets Management**
- No hardcoded secrets
- Environment variables used
- Sensitive data not logged
- PII handled correctly

✅ **Dependencies**
- No known vulnerable dependencies
- Dependencies up to date
- Minimal dependency footprint

**Red Flags:**
- ❌ Hardcoded passwords/API keys
- ❌ Direct SQL string concatenation
- ❌ Logging sensitive data (passwords, tokens)
- ❌ Missing authentication checks

### 5. Performance ⭐⭐

**Check for:**

✅ **Efficiency**
- No N+1 query problems
- Appropriate caching
- Async/await used correctly
- Database queries optimized

✅ **Resource Usage**
- Memory leaks prevented
- File handles closed
- Database connections managed
- Timeouts configured

**Example - N+1 Problem:**

```python
# ❌ Bad: N+1 queries
async def get_orders_with_items(user_id: str):
    orders = await order_repo.get_by_user(user_id)
    for order in orders:
        order.items = await item_repo.get_by_order(order.id)  # N queries!
    return orders

# ✅ Good: Single query with join
async def get_orders_with_items(user_id: str):
    return await order_repo.get_by_user_with_items(user_id)
```

### 6. Documentation ⭐⭐

**Check for:**

✅ **Code Comments**
- Complex logic explained
- Why, not what (code shows what)
- TODOs tracked with tickets
- Public APIs documented

✅ **Documentation Updates**
- README updated if needed
- API docs updated
- Event catalog updated
- Architecture docs current

✅ **Docstrings** (Python)
```python
def calculate_order_total(items: List[OrderItem]) -> Decimal:
    """
    Calculate total price for order items including tax.
    
    Args:
        items: List of order items with price and quantity
        
    Returns:
        Total amount including 10% tax
        
    Raises:
        ValueError: If any item has negative price or quantity
    """
```

## Review Checklist

Use this checklist when reviewing:

### Code Quality
- [ ] Code follows style guide (black/ruff for Python, Prettier for TS)
- [ ] Variable and function names are clear
- [ ] Functions are small and focused (< 50 lines)
- [ ] No code duplication
- [ ] Complex logic has comments
- [ ] Error handling is comprehensive
- [ ] Logging is appropriate

### Architecture
- [ ] Follows Clean Architecture layers
- [ ] Proper dependency injection
- [ ] Domain logic isolated from infrastructure
- [ ] Events follow schema conventions
- [ ] Database changes include migrations

### Testing
- [ ] New code has tests (>80% coverage)
- [ ] Edge cases are tested
- [ ] Error paths are tested
- [ ] Tests are clear and focused
- [ ] No flaky tests

### Security
- [ ] Input validation present
- [ ] No SQL injection vulnerabilities
- [ ] No hardcoded secrets
- [ ] Sensitive data not logged
- [ ] Authentication/authorization correct

### Performance
- [ ] No N+1 query problems
- [ ] Appropriate use of async/await
- [ ] Caching used where beneficial
- [ ] Database queries optimized

### Documentation
- [ ] PR description complete
- [ ] Complex code has comments
- [ ] API documentation updated
- [ ] Event catalog updated if needed
- [ ] README updated if needed

## Providing Feedback

### Be Constructive

**❌ Bad:**
```
This code is terrible.
```

**✅ Good:**
```
Consider extracting this logic into a separate method 
to improve readability and testability. Something like:

async def validate_payment_amount(amount: Decimal) -> None:
    if amount <= 0:
        raise ValueError("Amount must be positive")
```

### Be Specific

**❌ Bad:**
```
Fix the tests.
```

**✅ Good:**
```
The test `test_payment_processing` is flaky because it 
depends on system time. Consider using `freezegun` to 
mock the current time:

@freeze_time("2025-11-14")
async def test_payment_processing():
    # test code here
```

### Ask Questions

**Examples:**
```
Q: What happens if the payment gateway times out here?
Q: Why did we choose approach A over approach B?
Q: Could this cause a race condition with concurrent requests?
Q: Is there test coverage for this error path?
```

### Categorize Feedback

Use labels to indicate priority:

- **[Critical]**: Must fix (security, bugs)
- **[Important]**: Should fix (quality, architecture)
- **[Suggestion]**: Nice to have (optimization, style)
- **[Question]**: Seeking clarification

**Example:**
```
[Critical] This SQL query is vulnerable to injection.
Use parameterized queries instead.

[Important] Consider adding an index on `user_id` 
column for better query performance.

[Suggestion] Could simplify this with a list comprehension.

[Question] Why use sync here instead of async?
```

### Praise Good Work

Don't just point out issues - acknowledge good practices:

```
✨ Nice use of the Repository pattern here!
👍 Great test coverage for edge cases
💯 Excellent error messages - very helpful for debugging
🎯 Perfect use of feature flags for gradual rollout
```

## Responding to Feedback

### As an Author

**Do:**
- ✅ Thank reviewers for their time
- ✅ Ask questions if feedback unclear
- ✅ Explain reasoning if disagreeing
- ✅ Make requested changes promptly
- ✅ Mark conversations resolved when addressed
- ✅ Learn from feedback

**Don't:**
- ❌ Take feedback personally
- ❌ Argue defensively
- ❌ Ignore suggestions without response
- ❌ Make changes without discussion if you disagree

**Good Responses:**

```
Good catch! Updated to use parameterized query.
Fixed in commit abc123.

That's a good point. I went with approach A because
of X, but you're right that B might be better.
Let me refactor.

Interesting question - I used sync here because the
database client doesn't support async for this
operation yet. Added a TODO to migrate when upgraded.
```

### Resolving Disagreements

If you disagree with feedback:

1. **Understand**: Ask for clarification
2. **Explain**: Share your reasoning
3. **Discuss**: Have conversation in comments or sync call
4. **Decide**: Defer to senior developer or architect if needed
5. **Document**: Note decision and reasoning

**Example:**
```
I understand your concern about performance, but I
chose this approach for readability given our small
dataset (< 1000 records). Happy to optimize if you
think it's worth it, but wanted to explain the tradeoff.

What do you think?
```

## Common Issues

### Issue 1: Large Pull Requests

**Problem:** PR has 1000+ lines changed

**Solution:**
- Break into smaller PRs
- Review in parts (models first, then services, then APIs)
- Use draft PRs for work-in-progress
- Plan better task decomposition

**Guideline:** Target 200-400 lines per PR

### Issue 2: Insufficient Context

**Problem:** Can't understand changes without deep investigation

**Solution:**
- Write better PR descriptions
- Link to related tasks/issues
- Include screenshots for UI changes
- Explain "why" not just "what"

### Issue 3: Stale Branches

**Problem:** Branch diverged significantly from main

**Solution:**
- Rebase on main regularly
- Merge more frequently (smaller PRs)
- Close abandoned PRs
- Use feature flags to merge incomplete work

### Issue 4: Review Fatigue

**Problem:** Too many reviews, not enough time

**Solution:**
- Limit PR size
- Automate what can be automated (linting, tests)
- Schedule dedicated review time
- Rotate review responsibilities

## Best Practices

### For Authors

1. **Self-Review First**
   - Review your own code before requesting review
   - Check for common issues
   - Ensure tests pass
   - Verify documentation updated

2. **Small, Focused PRs**
   - One feature/fix per PR
   - Target 200-400 lines
   - Split large changes into sequence of PRs

3. **Good PR Description**
   ```markdown
   ## Description
   Implements payment retry mechanism with exponential backoff.
   
   ## Changes
   - Add retry logic to PaymentService
   - Implement exponential backoff calculator
   - Add circuit breaker for payment gateway
   - Update payment event schemas
   
   ## Testing
   - Unit tests for retry logic (100% coverage)
   - Integration tests with mock gateway
   - Manual testing of failure scenarios
   
   ## Related
   Closes TASK-042
   Part of US-002 (Payment Processing)
   ```

4. **Respond Quickly**
   - Address feedback within 24 hours
   - Mark conversations resolved
   - Push updates frequently

### For Reviewers

1. **Timely Reviews**
   - Review within 4 hours if possible
   - Block time for reviews
   - Don't let PRs go stale

2. **Constructive Feedback**
   - Be kind and respectful
   - Explain reasoning
   - Suggest improvements
   - Acknowledge good work

3. **Focus on Important Issues**
   - Prioritize security, bugs, architecture
   - Don't nitpick style (automate it)
   - Let some minor things go

4. **Ask Questions**
   - Seek to understand
   - Don't assume intent
   - Learn from the code

## Related Documentation

- [Version Control Workflow](version-control-workflow.md)
- [Coding Standards](coding-standards.md)
- [Testing Strategy](testing.md)
- [ADR-007: Trunk-Based Development](../adr/007-trunk-based-development.md)

---

**Questions?** Contact the Architecture Team on Slack #architecture channel.
