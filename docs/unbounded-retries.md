# Anti-Pattern: Unbounded Retries

An agent retries a failed action without a limit or a meaningful change in strategy.

Repeated identical attempts waste time and can amplify load on an unhealthy service. They also hide the original failure behind a long sequence of secondary errors.

Set a retry limit, use backoff for transient failures, and stop immediately for errors that another attempt cannot resolve. When retries are exhausted, preserve the last useful error and escalate or return control to the caller.