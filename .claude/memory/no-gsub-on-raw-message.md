# No gsub on the raw message field

Never use `mutate { gsub => ... }` on the raw `message` field before it is parsed. Parse
the event first (json, grok, or the codec), then mutate the structured fields.

**Why:** rewriting the raw line before parsing corrupts the input the parser depends on.
A `gsub` that looks harmless on one sample silently mangles another, and the failure
shows up far downstream as missing or wrong fields, which is exactly how detections go
blind (R-03).

**How to apply:** in a Logstash filter, put the `json`/`grok` parse first. Apply any
`mutate`, `gsub`, `rename`, or `add_field` only to the parsed fields afterwards. If you
think you need to clean the raw line, clean the specific parsed field instead.
