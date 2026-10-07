# Profile visuals

The profile uses indigo and teal accents, native technology logo colors, and light/dark variants. All displayed SVGs live in this repository.

## Automated assets

`.github/workflows/profile-visuals.yml` refreshes the stats, language cards and contribution snake daily at 03:17 UTC (06:17 in Türkiye). It can also be run manually from Actions.

- [GitHub Stats Extended](https://github.com/stats-organization/github-stats-extended) through [GitHub Readme Stats Action](https://github.com/stats-organization/github-readme-stats-action).
- [Platane/snk](https://github.com/Platane/snk) for the contribution snake.
- `scripts/prepare_snake.py` adds reduced-motion support to the generated animation.

Actions are pinned to commit SHAs; the stats core is pinned to 2.2.1. The workflow uses the built-in repository token and no additional secrets. It fails on a stats-fetch error so that the last successful cards remain available. Generated assets do not trigger another run.

The stats card labels its commit period. PR and star totals are cumulative. The language card measures code size in public, non-fork repositories, excluding this profile's generated SVGs. It is not a measure of proficiency or hours spent coding. These cards do not expose private repository details.

## Technology icons

The icon rows are composed from [Skill Icons](https://github.com/tandpfun/skill-icons) SVGs. Its MIT license is included in `assets/tech/LICENSE`. The LangChain, LangGraph, Qdrant and FAISS text labels were drawn for this profile. Text captions identify every tool without relying on logos alone.

## References

- [Average to PRO GitHub Profile](https://www.youtube.com/watch?v=Qng4TaXP904)
- [Snake Game on GitHub Profile](https://www.youtube.com/watch?v=U-IVndCqXWc)
- [GitHub's profile guide for job seekers](https://docs.github.com/en/account-and-profile/tutorials/using-your-github-profile-to-enhance-your-resume)
