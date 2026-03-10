# Requirements
- Python brush up
- Django Brush up
- PostgresSQL
- DocumentDB/ClickhouseDB/Redis
- RabbitMQ
- React / React Query

# Battle Plan

Day 1: Object-Oriented Design & State Management

This day focuses entirely on the 4-level simulation format. Your goal is to build clean classes, manage internal state, and write code that is easy to extend.

1. The In-Memory Database (The Core CodeSignal Simulation)

    Where to Practice: Search GitHub for "Mock CodeSignal Industry Coding Framework" (look for the repo by PaulLockett).

    The Drill: Do not use LeetCode for this one. Set a timer for 90 minutes and do this in your local IDE. Practice building a class that stores a dictionary of dictionaries (e.g., db[table_name][row_key] = {data}). Focus on implementing a set, get, and delete method, and then challenge yourself to add a rollback feature that reverts the state to 5 minutes ago.

2. Design In-Memory File System

    Where to Practice: LeetCode 588 (Premium, but widely mirrored on HackerRank and AlgoMonster).

    The Drill: You will need to implement ls, mkdir, addContentToFile, and readContentFromFile. The key here is to create a single Node class that acts as both a file and a directory, using a hash map to store its children.

3. Design a Text Editor

    Where to Practice: LeetCode 2296

    The Drill: You need to implement an editor with a cursor that can add text, delete text, and move left or right. The trick to keeping this performant is using two arrays (or stacks): one for the characters to the left of the cursor, and one for the characters to the right.

4. Design an ATM Machine

    Where to Practice: LeetCode 2241

    The Drill: You will manage deposits and withdrawals using 5 specific denominations ($20, $50, $100, $200, $500). This is a masterclass in greedy algorithms mixed with state management. Always fulfill withdrawals by aggressively pulling from the largest available denominations first.

Stepping away for a quick Slay the Spire run after wrapping up Day 1 can be a great way to let your brain passively process these heavy architecture patterns before jumping into the algorithms.
Day 2: Algorithmic Logic & Data Manipulation

Your deep background in AI/ML will make these data transformation problems feel like second nature, but during the interview, the goal is to write clean, readable code rather than the most mathematically clever one-liner.

5. Overlapping Computing Jobs (Merge Intervals)

    Where to Practice: LeetCode 56 (Merge Intervals)

    The Drill: You are given an array of intervals (start and end times) and must merge all overlapping ones. The golden rule here is to sort the array by the start times first. Once sorted, you only need to iterate through the list once, updating the "end time" of your current interval if the next one overlaps.

6. Merge Sorted Lists

    Where to Practice: LeetCode 23 (Merge k Sorted Lists)

    The Drill: You are given multiple linked lists that are already sorted, and you need to combine them into one massive sorted list. The most efficient way to solve this in an interview is by using a Priority Queue (Min-Heap). Push the head node of every list into the heap, pop the smallest one to add to your result, and then push that node's next value back into the heap.

7. Combinational Dice Rolls

    Where to Practice: LeetCode 1155 (Number of Dice Rolls With Target Sum) or LeetCode 77 (Combinations).

    The Drill: For Klaviyo, they often want you to physically output the combinations, not just count them. Practice writing a standard recursive backtracking function. You need a base case (e.g., "have I rolled n dice?"), and a for loop that iterates through the m faces, appending the current roll to a path array, recursing, and then popping it off to try the next face.

8. Array Transformation

    Where to Practice: LeetCode 189 (Rotate Array) or just use a local compiler.

    The Drill: This is usually a Level 1 or Level 2 warmup question. Practice iterating through an array a to build array b where b[i]=a[i−1]+a[i]+a[i+1]. The only trick is handling the IndexOutOfBounds exceptions safely at the first and last elements.


# Next
To practice the In-Memory Database specifically, you need to focus on state management and transaction tracking. Here are the best resources tailored precisely to that prompt:
1. The Exact Database Prompt on GitHub

    The zackdever/vsims Repository: This is almost a 1:1 match for the classic "Simple Database" question. It walks through implementing basic commands (SET, GET, UNSET, and NUMEQUALTO) for the early levels. More importantly, it covers the notoriously difficult Level 3 and 4 requirements: implementing nested transaction blocks (BEGIN, ROLLBACK, and COMMIT).

    The EricZheng0404/LibreSignal Repository: This is another recently updated, open-source simulator specifically built to mimic CodeSignal's Industry Coding Framework. It includes a local testing suite that forces you to build modular classes and pass hidden tests, which is exactly how the real 90-minute assessment will feel.

2. LeetCode Alternatives for Database Mechanics

While there is no single LeetCode question that mimics the entire 90-minute database project, you can use these specific problems to practice the hardest mechanics you will face in Levels 3 and 4:

    LeetCode 1146 (Snapshot Array): This is the best practice for the ROLLBACK requirement. It forces you to manage state changes over time and retrieve previous versions of your data efficiently without blowing up your memory limits.

    LeetCode 981 (Time Based Key-Value Store): This teaches you how to store multiple values for the same key based on timestamps. This pattern is critical if the assessment asks you to implement a Time-To-Live (TTL) feature where database keys automatically expire after a certain duration.

A Quick Architecture Tip for the Test

When you inevitably reach the BEGIN / ROLLBACK / COMMIT stage, the biggest trap candidates fall into is trying to duplicate the entire database dictionary every time a transaction starts. That will trigger a Memory Limit Exceeded error on the hidden test cases.

Instead, maintain a stack of "transaction logs". When a user modifies a key during an active transaction, only save the old value of that specific key to the top of the stack. If they call ROLLBACK, pop that log and restore only those specific keys.

# Resources
https://github.com/PaulLockett/CodeSignal_Practice_Industry_Coding_Framework/tree/main
https://github.com/EricZheng0404/LibreSignal/tree/main
https://github.com/zackdever/vsims
