/**
 * @type {import('semantic-release').GlobalConfig}
 */
module.exports = {
  branches: ["main", "next"],
  plugins: [
    [
      "@semantic-release/commit-analyzer",
      {
        preset: "angular",
        releaseRules: [
          {
            breaking: true,
            release: "major",
          },
          {
            type: "feat",
            release: "minor",
          },
          {
            type: "fix",
            release: "patch",
          },
          {
            type: "docs",
            scope: "README",
            release: "patch",
          },
          {
            type: "chore",
            release: "patch",
          }
        ],
        parserOpts: {
          noteKeywords: ["BREAKING CHANGE", "BREAKING CHANGES", "BREAKING"],
        },
      },
    ],
    [
      "@semantic-release/release-notes-generator",
      {
        /*  
            use conventionalcommits instead of conventional-changelog-angular (default)
            to introduce new sections in changelog
        */
        preset: "conventionalcommits",
        presetConfig: {
          types: [
            { type: "feat", section: "Features", hidden: false },
            { type: "fix", section: "Bug Fixes", hidden: false },
            { type: "docs", section: "Miscellaneous Chores", hidden: false },
            { type: "chore", section: "Miscellaneous Chores", hidden: false },
          ],
        },
        parserOpts: {
          noteKeywords: ["BREAKING CHANGE", "BREAKING CHANGES", "BREAKING"],
        },
      },
    ],
    ["@semantic-release/npm"],
    [
      "@semantic-release/changelog",
      {
        changelogFile: "CHANGELOG.md",
      },
    ],
    [
      "@semantic-release/git",
      {
        assets: ["package.json", "CHANGELOG.md"],
      },
    ],
    "@semantic-release/gitlab",
  ],
};
