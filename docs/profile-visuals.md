# Profile visuals

The profile follows the portfolio palette: navy, ice blue and lime, with readable light-mode variants and native technology logo colors. All displayed SVGs live in this repository.

The static engineering drawing has separate wide (900 × 96) and narrow (450 × 96) compositions. Names, the professional title, project descriptions and links remain selectable Markdown text.

## Automated assets

`.github/workflows/profile-visuals.yml` refreshes the stats, language cards and contribution snake daily at 03:17 UTC (06:17 in Türkiye). It can also be run manually from Actions.

- [GitHub Stats Extended](https://github.com/stats-organization/github-stats-extended) through [GitHub Readme Stats Action](https://github.com/stats-organization/github-readme-stats-action).
- [Platane/snk](https://github.com/Platane/snk) for the contribution snake.
- `scripts/prepare_snake.py` decorates the generated route with direction-aware eyes, a forked tongue, a small eating reaction and bounded body growth. It retains reduced-motion support.

Actions are pinned to commit SHAs; the stats core is pinned to 2.2.1. The workflow uses the built-in repository token and no additional secrets. It fails on a stats-fetch error so that the last successful cards remain available. Generated assets do not trigger another run.

The stats card labels its commit period. PR and star totals are cumulative. The language card measures code size in public, non-fork repositories, excluding this profile's generated SVGs. It is not a measure of proficiency or hours spent coding. These cards do not expose private repository details.

## Snake behavior

The original contribution grid, clearing times, route and collection bar come from the pinned Platane generator. The decorator reads the head keyframes and cell-clearing events, then builds overlapping trailing body pieces on the same path. The body starts at roughly four cells long and gradually grows to at most twelve; growth is a visual interpretation, not a change to the upstream path-finding solver. A cell consumption briefly opens the mouth and lights a small ring at that cell. The face turns with the route and the tongue flicks periodically. The loop resets its growth during the return path. With reduced motion, the graph and a short, still snake remain visible while flashes and the tongue are hidden.

If the expected upstream SVG structure changes, decoration fails rather than silently producing a broken animation; the workflow retains the last successful assets.

## Technology icons

The icon rows are composed from [Skill Icons](https://github.com/tandpfun/skill-icons) SVGs. Its MIT license is included in `assets/tech/LICENSE`. The LangChain, LangGraph, Qdrant and FAISS text labels were drawn for this profile. Individual 32 px tiles wrap naturally on narrow screens. Each has descriptive alternative text; the full names also appear in the expandable Full stack section.

## References

- [Average to PRO GitHub Profile](https://www.youtube.com/watch?v=Qng4TaXP904)
- [Snake Game on GitHub Profile](https://www.youtube.com/watch?v=U-IVndCqXWc)
- [GitHub's profile guide for job seekers](https://docs.github.com/en/account-and-profile/tutorials/using-your-github-profile-to-enhance-your-resume)
