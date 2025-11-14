# Task Template (ClickUp)

> **Note**: This template is used to generate technical tasks from user stories. Tasks are written in English for international team collaboration.

---

## Task Format

```markdown
## [TASK-XXX] Task Title (Imperative Verb + Noun)

**Related User Story**: US-XXX - User Story Title  
**Epic**: Epic Name  
**Priority**: 🔴 High / 🟡 Medium / 🟢 Low  
**Story Points**: X points  
**Assignee**: TBD  
**Sprint**: Sprint X  

---

### 📋 Description

[Clear description of what needs to be implemented. Include technical context and rationale.]

**Technical Scope**:
- Component/Service affected: [service-name]
- Files to modify/create: [list key files]
- Dependencies: [external services, libraries, or other tasks]

---

### ✅ Functional Acceptance Criteria

- [ ] **AC1**: [User-facing functionality criteria]
- [ ] **AC2**: [Another functional requirement]
- [ ] **AC3**: [Edge case or error handling]

**Example**:
- [ ] User can submit an order through POST /api/orders endpoint
- [ ] System returns 201 Created with order ID in response body
- [ ] Invalid input returns 400 Bad Request with validation errors

---

### 🔧 Technical Acceptance Criteria

- [ ] **TAC1**: [Code quality requirement - unit tests]
- [ ] **TAC2**: [Performance requirement]
- [ ] **TAC3**: [Security requirement]
- [ ] **TAC4**: [Documentation requirement]
- [ ] **TAC5**: [Observability requirement]

**Example**:
- [ ] Unit test coverage ≥ 80% for new code
- [ ] API response time < 200ms (p95)
- [ ] Input validation using FluentValidation
- [ ] OpenAPI/Swagger documentation updated
- [ ] Structured logging with correlation IDs implemented
- [ ] Integration test for happy path and error scenarios

---

### 🏗️ Best Practices to Apply

**Architecture**:
- [ ] Follow Clean Architecture layers (Domain → Application → Infrastructure)
- [ ] Implement CQRS pattern if applicable (separate read/write models)
- [ ] Use Repository pattern for data access
- [ ] Apply Dependency Inversion (interfaces in domain, implementations in infrastructure)

**Code Quality**:
- [ ] Follow SOLID principles
- [ ] Use meaningful variable and method names (no abbreviations unless standard)
- [ ] Keep methods small (< 20 lines ideally)
- [ ] One level of abstraction per function
- [ ] Extract magic numbers/strings to constants

**Event-Driven**:
- [ ] Publish events using domain events pattern
- [ ] Include correlation ID and causation ID in event envelope
- [ ] Implement idempotency for event handlers (check if already processed)
- [ ] Use outbox pattern for reliable event publishing
- [ ] Version events using semantic versioning (v1, v2, etc.)

**Resilience**:
- [ ] Implement circuit breaker for external calls
- [ ] Add retry policy with exponential backoff
- [ ] Set appropriate timeouts
- [ ] Handle transient failures gracefully

**Security**:
- [ ] Validate all inputs (never trust user input)
- [ ] Sanitize outputs to prevent injection attacks
- [ ] Use parameterized queries (no string concatenation for SQL)
- [ ] Implement proper authentication/authorization
- [ ] Don't log sensitive data (passwords, tokens, PII)

**Testing**:
- [ ] Write unit tests first (TDD approach recommended)
- [ ] Test edge cases and error paths
- [ ] Use test doubles (mocks/stubs) appropriately
- [ ] Integration tests for external dependencies
- [ ] Contract tests for events published/consumed

**Observability**:
- [ ] Structured logging with Serilog
- [ ] Log at appropriate levels (Trace/Debug/Info/Warning/Error/Critical)
- [ ] Include correlation ID in all logs
- [ ] Add metrics for key operations (duration, count, errors)
- [ ] Implement health checks

---

### 💡 Recommendations

**Before Starting**:
1. Review the User Story and clarify any ambiguities with Product Owner
2. Check existing codebase for similar implementations to follow patterns
3. Review related ADRs (Architecture Decision Records)
4. Identify dependencies and coordinate with other team members
5. Break down into smaller sub-tasks if estimated > 5 story points

**During Implementation**:
1. Commit frequently with meaningful messages (conventional commits format)
2. Run tests locally before pushing
3. Update documentation as you code (don't leave it for the end)
4. Ask for help early if blocked (don't wait days)
5. Consider pair programming for complex logic

**Code Review Checklist**:
1. Self-review your code before requesting review
2. Ensure all tests pass in CI/CD pipeline
3. Check for console.log / debug statements to remove
4. Verify no sensitive data in code or commits
5. Update CHANGELOG.md with notable changes

**After Completion**:
1. Demo the feature to the team (show, don't tell)
2. Update technical documentation if architecture changed
3. Share learnings in team retrospective
4. Monitor production logs/metrics after deployment

---

### 🔗 Related Resources

- **User Story**: [Link to BACKLOG.md#US-XXX]
- **Architecture Doc**: [Link to relevant architecture doc]
- **ADR**: [Link to relevant ADR if applicable]
- **Event Specification**: [Link to event catalog entry]
- **API Documentation**: [Link to Swagger/OpenAPI spec]
- **Design Doc**: [Link to technical design if exists]

---

### 📝 Implementation Notes

[Space for developer to add notes during implementation]

**Questions**:
- [ ] Question 1: [Question for PO/Tech Lead]

**Technical Decisions**:
- Decision 1: [Rationale for technical choice made]

**Blockers**:
- [ ] Blocker 1: [Description and mitigation plan]

---

### 🧪 Testing Strategy

**Unit Tests**:
- Test 1: [Scenario to test]
- Test 2: [Edge case]

**Integration Tests**:
- Test 1: [Full flow to test]

**Manual Testing**:
- [ ] Step 1: [How to verify manually]
- [ ] Step 2: [Expected result]

---

### 🚀 Deployment Notes

**Prerequisites**:
- [ ] Database migration script created (if needed)
- [ ] Configuration changes documented
- [ ] Feature flag added (if applicable)

**Rollback Plan**:
- [ ] Revert commit: [commit hash]
- [ ] Rollback database: [migration name]

---

### ✅ Definition of Done

- [ ] Code implemented and follows coding standards
- [ ] All acceptance criteria met (functional + technical)
- [ ] Unit tests written and passing (coverage ≥ 80%)
- [ ] Integration tests passing
- [ ] Code reviewed and approved
- [ ] Documentation updated (README, API docs, ADRs if needed)
- [ ] Merged to main branch
- [ ] Deployed to staging and verified
- [ ] Demo completed with stakeholders
- [ ] Monitoring/alerts configured
```

---

## Example Task

```markdown
## [TASK-001] Implement Create Order API Endpoint

**Related User Story**: US-001 - Creación de Pedido Básico  
**Epic**: Order Management  
**Priority**: 🔴 High  
**Story Points**: 5 points  
**Assignee**: TBD  
**Sprint**: Sprint 1  

---

### 📋 Description

Implement the REST API endpoint to create a new order in the Orders API service. This endpoint receives order details from the client, validates the input, persists the order to OrdersDB, and publishes an OrderCreatedEvent to notify other services.

**Technical Scope**:
- Component/Service affected: orders-api
- Files to modify/create:
  - `src/api/controllers/OrdersController.cs` (new)
  - `src/application/commands/CreateOrderCommand.cs` (new)
  - `src/application/handlers/CreateOrderCommandHandler.cs` (new)
  - `src/domain/entities/Order.cs` (new)
  - `src/infrastructure/persistence/OrderRepository.cs` (new)
- Dependencies: 
  - MassTransit for event publishing
  - SQL Server for persistence
  - FluentValidation for input validation

---

### ✅ Functional Acceptance Criteria

- [ ] **AC1**: Client can submit order via POST /api/v1/orders with customerId, items array (productId, quantity, price)
- [ ] **AC2**: System validates input (required fields, positive quantities, valid customer ID format)
- [ ] **AC3**: System returns 201 Created with orderId, orderNumber, totalAmount, createdAt in response
- [ ] **AC4**: Invalid input returns 400 Bad Request with detailed validation errors
- [ ] **AC5**: If customer ID doesn't exist, return 404 Not Found
- [ ] **AC6**: System calculates totalAmount as sum of (quantity × price) for all items

---

### 🔧 Technical Acceptance Criteria

- [ ] **TAC1**: Unit test coverage ≥ 80% for command handler and domain logic
- [ ] **TAC2**: API response time < 200ms at p95 (under normal load)
- [ ] **TAC3**: Input validation using FluentValidation with custom rules
- [ ] **TAC4**: OpenAPI/Swagger documentation includes request/response schemas and examples
- [ ] **TAC5**: Structured logging with correlation ID, order ID, customer ID
- [ ] **TAC6**: Integration test covering happy path and validation errors
- [ ] **TAC7**: OrderCreatedEvent published to message broker with correct schema (see event catalog)
- [ ] **TAC8**: Database transaction ensures atomicity (order + event outbox)

---

### 🏗️ Best Practices to Apply

**Architecture**:
- [x] Follow Clean Architecture layers
- [x] Implement CQRS pattern (this is a Command)
- [x] Use Repository pattern for Order persistence
- [x] Apply Dependency Inversion (IOrderRepository interface)

**Code Quality**:
- [x] Follow SOLID principles (especially SRP and OCP)
- [x] Use meaningful names: `CreateOrderCommand`, `OrderCreatedEvent`
- [x] Keep handler method focused (delegate validation and persistence)
- [x] Extract order total calculation to domain method

**Event-Driven**:
- [x] Publish OrderCreatedEvent using domain events pattern
- [x] Include correlationId, causationId in event envelope
- [x] Use outbox pattern (save event to DB, then publish)
- [x] Event schema version v1 (see docs/events/orders/OrderCreatedEvent.md)

**Resilience**:
- [x] Set timeout for database operations (5 seconds)
- [x] Handle transient DB failures with retry (use Polly)

**Security**:
- [x] Validate customerId format (GUID)
- [x] Validate quantity > 0 and price ≥ 0
- [x] Use parameterized queries via EF Core
- [x] Don't log payment details (not in scope but note for future)

**Testing**:
- [x] TDD: Write failing test first
- [x] Test validation errors (missing fields, negative quantities)
- [x] Mock IOrderRepository for unit tests
- [x] Integration test with test database

**Observability**:
- [x] Log at Information level: "Order created successfully: {OrderId}"
- [x] Log at Warning level: "Order creation failed validation: {Errors}"
- [x] Include correlationId from HTTP header in all logs
- [x] Add metric: orders_created_total (counter)
- [x] Health check for database connection

---

### 💡 Recommendations

**Before Starting**:
1. Review US-001 in BACKLOG.md for business context
2. Check docs/architecture/README.md for Orders API responsibilities
3. Review docs/events/orders/OrderCreatedEvent.md for event schema
4. Set up local SQL Server database (use Docker if needed)

**During Implementation**:
1. Start with domain model (Order entity) - it has no dependencies
2. Then create command and validator
3. Implement handler with repository
4. Add controller endpoint
5. Write tests alongside (TDD)

**Code Review Checklist**:
1. Verify OrderCreatedEvent matches schema in event catalog
2. Check that validation messages are user-friendly
3. Ensure repository uses async/await properly
4. Confirm transaction scope includes event outbox

---

### 🔗 Related Resources

- **User Story**: [BACKLOG.md#US-001](../BACKLOG.md#us-001-creación-de-pedido-básico)
- **Architecture Doc**: [docs/architecture/README.md](../docs/architecture/README.md)
- **Event Specification**: [docs/events/orders/OrderCreatedEvent.md](../docs/events/orders/OrderCreatedEvent.md)
- **Service Context**: [services/orders-api/.copilot-context.md](../services/orders-api/.copilot-context.md)

---

### ✅ Definition of Done

- [ ] Code implemented and follows coding standards
- [ ] All acceptance criteria met (6 functional + 8 technical)
- [ ] Unit tests written (≥80% coverage)
- [ ] Integration test passing
- [ ] Code reviewed and approved by 2 team members
- [ ] Swagger documentation verified
- [ ] Merged to main branch
- [ ] Deployed to staging and smoke tested
- [ ] Demo completed with Product Owner
```

---

## Naming Conventions

- **Task ID**: `TASK-XXX` (sequential number)
- **Title Format**: Verb + Noun (e.g., "Implement Create Order API", "Refactor Event Handler")
- **Common Verbs**: Implement, Create, Update, Refactor, Fix, Add, Remove, Configure, Deploy, Test
- **Be Specific**: "Implement Order Creation API Endpoint" > "Work on Orders"
