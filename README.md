# Pink Neurons - Visual Learning Platform

A beautiful and interactive platform letting you enter the realm of learning CS + Math concepts through the very famous Manim visualisations.

## What is Manim?
[Manim](https://www.manim.community/) (Mathematical Animation Engine) is an open-source Python library created by Grant Sanderson, the brilliant mind behind the popular YouTube channel 3Blue1Brown. Originally developed to create the stunning mathematical animations seen in his educational videos, Manim allows developers and educators to programmatically generate precise, visually engaging animations that explain complex concepts with remarkable clarity. 

## How It Works
![image](https://github.com/user-attachments/assets/4191d0b9-d7c3-4a7b-8ce7-325449f1f9b4)

## Output We Generated (: :

![videoplayback](https://github.com/user-attachments/assets/4a909c03-d6d7-4853-95ac-0b11adad76f0)

## How to Run

1. Make sure you have the Manim environment activated:

```bash
conda activate manim
```

2. Install the required dependencies:

```bash
pip install requests manim
```

3. Run the included server script:

```bash
python server.py
```

4. The website will open automatically, or you can navigate to:
```
http://localhost:8000
```

## Usage

- Click on any topic button on the right side to watch the embedded video
- Use the search box on the left to find specific topics
- Enter custom learning topics in the search field
- Close videos by clicking the X, clicking outside the video, or pressing ESC
- **NEW**: Search for topics not in the popular list to generate a custom Manim visualization

## Testing Custom Visualizations

You can test the visualization generation separately using the test script:

```bash
python test_render.py "quick sort"
```

Replace "quick sort" with any DSA topic you want to visualize.

## Structure

- `index.html`: Main webpage content
- `styles.css`: Styling for the website
- `script.js`: JavaScript for interactivity
- `server.py`: Simple Python server with API endpoints
- `openrouter_api.py`: Client for generating Manim code with Optimus Alpha
- `manim_renderer.py`: Tools for rendering Manim animations
- `test_render.py`: Test script for generating and rendering animations
- `img/team_logo.png`: Pink Neurons logo

## Technology

- Frontend: HTML5, CSS3, JavaScript
- Backend: Python
- Animation: Manim (Mathematical Animation Engine)
- AI Code Generation: OpenRouter.ai's Optimus Alpha model

## Note

Before running, ensure that:
1. The logo image is saved as "img/team_logo.png"
2. You have a working installation of Manim
3. You have internet connectivity for OpenRouter API calls 
