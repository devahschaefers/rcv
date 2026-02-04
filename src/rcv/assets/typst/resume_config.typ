// Common Typst configuration and helper macros for resumes.

// Page and typography
// Adjust margins to roughly mirror the LaTeX preamble defaults.
// 1in ~= 2.54cm; we mirror 1.06cm sides and 1.7cm top.
// Use a clean sans-serif; change as you prefer.
// Feel free to override in your resume files.
//
// Example usage inside a resume:
//   #import "../assets/typst/resume_config.typ": *
//   #set page(margin: page_margins)
//   #set text(text_style)

// Margins and base text settings
let page_margins = (
  left: 1.06cm,
  right: 1.06cm,
  top: 1.7cm,
  bottom: 0.49cm,
)

let text_style = (
  font: "Helvetica",
  size: 11pt,
  hyphenate: false,
)

// Header helpers
// Centered header area with horizontally spaced items.
// Usage:
//   #header([
//     link("https://linkedin.com/in/devahschaefers", text(["LinkedIn ", sym.linkedin()])),
//     link("https://github.com/devahschaefers", text(["GitHub ", sym.github()])),
//     link("https://gitlab.com/devahschaefers", text(["GitLab ", sym.gitlab()])),
//   ])
let header(items) = {
  align(center)[
    for (i, item) in items.enumerate() {
      item
      if i < items.len() - 1 { h(1.5em) }
    }
  ]
}

// Section title style with rules on either side (similar to the LaTeX preamble)
let section_title(title) = {
  block(
    spacing: 0pt,
    align(center)[
      line(length: 1fr, stroke: 0.4pt)
      h(0.75em)
      strong(title)
      h(0.75em)
      line(length: 1fr, stroke: 0.4pt)
    ],
    inset: (top: 4pt, bottom: 4pt),
  )
}

// Experience block helper similar to the LaTeX \experienceblock macro
// Params: role, location, org, dates, language (optional)
let experience_block(role, location, org, dates, language: none) = {
  block(
    spacing: 2pt,
    strong(role) + hfill() + org,
    if language != none { emph(language) + hfill() + dates } else { dates },
    emph(location),
  )
}

// Small vertical spacer, mirrors \blocksep
let block_sep = v(2pt)

// Lists: tighter item spacing
#set list(spacing: 2pt, tight: true)

// Links: neutral styling (uncomment to customize for your Typst version)
// #show link: it => text(fill: black)[it]
