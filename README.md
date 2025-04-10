# ENG1013 Team MA04

A central repository to manage and track each team member's source code and circuit diagrams.

## Repository Structure

```
team-code-tracker/
├── source_code/
│   ├── subsystem1/
│   ├── subsystem2/
│   └── ...
└── circuit_diagrams/
    ├── subsystem1/
    ├── subsystem2/
    └── ...
```

## Branch Structure

This repository maintains two primary branches:
1. `milestone2` - The branch for resources related to milestone 2
2. `milestone3` - The branch for resources related to milestone 3

All team members are expected to work on both branches according to the workflow described below.

## Getting Started

### To work on the project

1. Clone this repository:
   ```
   git clone https://github.com/Tang0711/ENG1013_Team_MA04.git
   ```

2. Set up both branches locally:
   ```
   git fetch origin
   git checkout milestone2
   git checkout milestone3
   ```

3. Create your personal folders:
   ```
   git checkout milestone2
   mkdir source_code/the-subsystem
   mkdir circuit_diagrams/the-subsystem
   ```

4. Commit and push your changes:
   ```
   git add .
   git commit -m "Changes for subsystem x"
   git push origin <branch>
   ```

## Working with Branches

### milestone2 Branch
- Use for milestone2 development work and updates

### Main Branch
- Use for milestone2 development work and updates

## File Organization

### Source Code
- Place all your code files in your designated folder in `source_code/the-subsystem/`
- Name the file as the name of subsystems
- Follow [coding standards](https://drive.google.com/file/d/12PV9XTidXxmY8kKtBtORh3R1JKq6OpJP/view?usp=sharing)

### Circuit Diagrams
- Store all circuit diagrams in your folder in `circuit_diagrams/the-subsystem/`
- Accepted formats: .png, .jpg, and .svg
- Follow [circuit standards](https://docs.google.com/document/d/1SD0AerNVj7wxJGq-ChEapkl0-5x0M4dbt7Ev7d3fn-4/edit?usp=sharing)

## Code Review Process

1. Push your changes to the related branch
2. Create a pull request to the appropriate target branch
3. Request review from Wei Zhi or Yao Ren
4. Address any feedback
5. Merge once approved

## Commit Guidelines

Write clear commit messages describing your changes:
```
[AREA]: Brief description of changes

More detailed explanation if needed
```

Areas include: CODE, CIRCUIT, etc.

## Contact

For questions or assistance, contact the repository administrator:
- Name: Wei Zhi
- Phone number: 011-59601080