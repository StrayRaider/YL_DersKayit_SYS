import graphviz

# Create a new Digraph (Directed Graph)
dot = graphviz.Digraph(format='png')

# Start node
dot.node('start', 'Start')

# Initialize Variables
dot.node('init_vars', 'Initialize Variables')
dot.edge('start', 'init_vars')

# Define Notes
dot.node('define_notes', 'Define Notes')
dot.edge('init_vars', 'define_notes')

# Split Data
dot.node('split_data', 'Split Data')
dot.edge('define_notes', 'split_data')

# Iterate Over Lessons
dot.node('iterate_lessons', 'Iterate Over Lessons')
dot.edge('split_data', 'iterate_lessons')

# Check LessonL Length
dot.node('check_length', 'Check LessonL Length')
dot.edge('iterate_lessons', 'check_length')

# Append LessonL to LessonList
dot.node('append_lesson_list', 'Append LessonL to LessonList')
dot.edge('check_length', 'append_lesson_list')

# Display LessonList
dot.node('display_list', 'Display LessonList')
dot.edge('append_lesson_list', 'display_list')

# Iterate Over LessonList
dot.node('iterate_list', 'Iterate Over LessonList')
dot.edge('display_list', 'iterate_list')

# End node
dot.node('end', 'End')
dot.edge('iterate_list', 'end')

# Render the flowchart to a PNG file
dot.render('flowchart', view=True)

