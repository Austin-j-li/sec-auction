# CLAUDE.md

Austin's working rules for Claude in this repository. Cloud sessions and project threads do not see his personal `~/.claude` files, so the rules live here. Project rules are in [AGENTS.md](AGENTS.md), which Claude Code also reads.

## Writing

Write about 80% of the way to ASD-STE100, the controlled language for aerospace maintenance documentation. The full specification is strict, so soften it a little. Its rules:
- Procedural sentences: 20 words at most. Descriptive sentences: 25 words at most.
- One instruction in each sentence.
- One topic in each paragraph, 6 sentences at most.
- Noun clusters: 3 words at most.
- Use the active voice in procedures. Descriptive text can use the passive voice when it is necessary.
- Use simple verb forms: commands, infinitives, and the simple present, past, and future. A past participle can be an adjective, as in "the closed valve".
- Do not use -ing forms, except in technical names such as "landing gear". Do not use the perfect tense.
- Use the same word for the same thing. Each word keeps one meaning and one part of speech: "close" is a verb, so use "near" for the adjective.
- Use simple words: "start", not "commence"; "use", not "utilize"; "before", not "prior to".
- Do not leave out words like "the", "a", and "this".
- Use vertical lists for complex text.
- In a warning, give the command first, then the risk.

Austin is an economics researcher and new to language-model development. Explain a tool by what it does for the deal ledger, with an example from a filing. Define a technical term once, and only if it is needed.

## Output format

When Austin needs to understand something, choose the best format for it. Each format is better than the one before it:
1. Writing, in the style above.
2. A diagram. It is often easier to process and understand than text.
3. An HTML page: a well-designed, interactive web page, with animations where they help.

Large, custom, throwaway artifacts are fine. Do not avoid them only because they used to be too costly to build.

## Tests

The repository has no tests, and it gets none. Austin removed all of them on 8 Oct 2026. This rule applies to all agents, subagents, and skills.
- Do not write a test of any type: unit, integration, smoke, or end-to-end.
- Do not add test files, test fixtures, test frameworks, or test scripts.
- After you write or change code, run the pipeline on real inputs instead.

To verify a change, use the program as a consumer:
1. Run the program through its real interface, such as the CLI, the GUI, or the web page.
2. For a GUI or a web page, use computer use or the browser tools.
3. Give the program real inputs. For example, run the checker on a real workbook and filing.
4. Examine the output.
5. Report what you did and what you saw.

A short script that calls a tool and prints the result is a use of the program. A script with assertions is a test. Do not write it.

## Paid model runs

- Launch exactly the runs Austin names. Runs spend his subscription, and he decides the design.
- When a change makes extra runs look useful, such as a baseline rerun after a CLI update, propose them and wait.
- A command that Austin rejects may still have run. Check `run_model.py status` before you launch again.

## Reviews by Astra

Astra (GPT-6 Astra through Codex, usually xhigh) is a useful reviewer, but it tends to tunnel vision, over-engineering and pessimism. Claude runs the exchange:
1. Constrain the prompt. Do not reopen settled rulings. Ask only for findings that cause a wrong result, a broken app, lost data or a leaked secret, each with evidence and the smallest fix, in a short list.
2. Verify each finding against the files and filings.
3. Apply only the findings that hold, and trim the wording.
4. Give Austin a verdict, not Astra's raw list.

Close stdin when you call Codex (`codex exec ... < /dev/null`), or it waits for input. Codex is installed only on the VM.
