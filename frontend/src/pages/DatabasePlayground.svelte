<script lang="ts">
  import { onMount } from 'svelte';
  import { Link } from 'svelte-routing';
  import Footer from '../lib/components/layout/Footer.svelte';
  import SkeletonLoader from '../lib/components/loaders/SkeletonLoader.svelte';
  import CustomSelect from '../lib/components/CustomSelect.svelte';
  import { fadeSlide } from '../lib/utils/transitions';
  
  interface QuizQuestion {
    id: number;
    question: string;
    difficulty: string;
    points: number;
    category: string;
  }
  
  interface LeaderboardEntry {
    rank: number;
    username: string;
    score: number;
    time_taken: number;
    completed_at: string;
  }
  
  let quizStarted = false;
  let quizCompleted = false;
  let questions: QuizQuestion[] = [];
  let currentQuestionIndex = 0;
  let userQuery = '';
  let score = 0;
  let feedback = '';
  let loading = false;
  let showAnswer = false;
  let expectedQuery = '';
  let username = '';
  let startTime = 0;
  let elapsedTime = 0;
  let timerInterval: any = null;
  let leaderboard: LeaderboardEntry[] = [];
  let loadingLeaderboard = false;
  let userStats = { rank: null, score: 0, time_taken: 0 };
  let questionCount = 10;
  let difficulty = '';
  let showLeaderboard = false;
  
  $: currentQuestion = questions[currentQuestionIndex];
  $: progress = questions.length > 0 ? ((currentQuestionIndex + 1) / questions.length * 100) : 0;
  
  async function startQuiz() {
    if (!username || username.length < 2) {
      alert('Please enter a username (at least 2 characters)');
      return;
    }
    
    loading = true;
    try {
      const url = difficulty 
        ? `/api/quiz/questions?count=${questionCount}&difficulty=${difficulty}`
        : `/api/quiz/questions?count=${questionCount}`;
      
      const res = await fetch(url);
      questions = await res.json();
      
      if (questions.length === 0) {
        alert('No questions available');
        return;
      }
      
      quizStarted = true;
      startTime = Date.now();
      
      timerInterval = setInterval(() => {
        elapsedTime = Math.floor((Date.now() - startTime) / 1000);
      }, 1000);
      
    } catch (error) {
      alert('Failed to load quiz questions');
    } finally {
      loading = false;
    }
  }
  
  async function submitAnswer() {
    if (!userQuery.trim()) {
      feedback = 'Please enter a SQL query';
      return;
    }
    
    loading = true;
    feedback = '';
    showAnswer = false;
    
    try {
      const res = await fetch('/api/quiz/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question_id: currentQuestion.id,
          user_query: userQuery
        })
      });
      
      const data = await res.json();
      
      if (data.correct) {
        score += data.points_earned;
        feedback = data.feedback;
      } else {
        feedback = data.feedback;
        expectedQuery = data.expected_query || '';
        showAnswer = true;
      }
      
    } catch (error) {
      feedback = 'Error validating answer';
    } finally {
      loading = false;
    }
  }
  
  function nextQuestion() {
    if (currentQuestionIndex < questions.length - 1) {
      currentQuestionIndex++;
      userQuery = '';
      feedback = '';
      showAnswer = false;
      expectedQuery = '';
    } else {
      finishQuiz();
    }
  }
  
  async function finishQuiz() {
    clearInterval(timerInterval);
    quizCompleted = true;
    
    const timeTaken = Math.floor((Date.now() - startTime) / 1000);
    
    try {
      await fetch('/api/quiz/leaderboard/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username,
          score,
          time_taken: timeTaken
        })
      });
      
      await loadLeaderboard();
      await loadUserStats();
    } catch (error) {
      console.error('Failed to submit score:', error);
    }
  }
  
  async function loadLeaderboard() {
    loadingLeaderboard = true;
    try {
      const res = await fetch('/api/quiz/leaderboard?limit=10');
      leaderboard = await res.json();
    } catch (error) {
      console.error('Failed to load leaderboard');
    } finally {
      loadingLeaderboard = false;
    }
  }
  
  async function loadUserStats() {
    try {
      const res = await fetch(`/api/quiz/user-stats/${username}`);
      userStats = await res.json();
    } catch (error) {
      console.error('Failed to load user stats');
    }
  }
  
  function restartQuiz() {
    quizStarted = false;
    quizCompleted = false;
    questions = [];
    currentQuestionIndex = 0;
    userQuery = '';
    score = 0;
    feedback = '';
    showAnswer = false;
    expectedQuery = '';
    elapsedTime = 0;
  }
  
  function formatTime(seconds: number): string {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  }
  
  onMount(() => {
    loadLeaderboard();
  });
</script>

<div class="container mx-auto px-4 py-24">
  <h1 class="text-4xl font-bold mb-6 text-gradient">
    SQL Quiz Challenge
  </h1>
  <p class="text-gray-400 mb-12 text-lg">
    Test your SQL knowledge with {questions.length || questionCount} questions. Compete for the top spot on the leaderboard!
  </p>
  
  <div class="max-w-7xl mx-auto px-6">
  {#if !quizStarted && !quizCompleted}
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
      <div class="card">
        <h3 class="text-2xl font-bold mb-6 text-white">🎯 Start Quiz</h3>
        
        <div class="space-y-6">
          <div>
            <label for="username-input" class="block text-sm font-medium mb-2">Your Username</label>
            <input
              id="username-input"
              type="text"
              bind:value={username}
              placeholder="Enter your username..."
              class="w-full bg-gray-900 border border-white/20 rounded-lg px-4 py-3"
            />
          </div>
          
          <div>
            <label for="question-count" class="block text-sm font-medium mb-2">Number of Questions</label>
            <CustomSelect
              id="question-count"
              bind:value={questionCount}
              options={[
                { value: 5, label: '5 Questions' },
                { value: 10, label: '10 Questions' },
                { value: 15, label: '15 Questions' },
                { value: 20, label: '20 Questions' }
              ]}
            />
          </div>
          
          <div>
            <label for="difficulty-select" class="block text-sm font-medium mb-2">Difficulty (Optional)</label>
            <CustomSelect
              id="difficulty-select"
              bind:value={difficulty}
              options={[
                { value: '', label: 'All Difficulties (Mixed)' },
                { value: 'easy', label: 'Easy (10 points)' },
                { value: 'medium', label: 'Medium (20 points)' },
                { value: 'hard', label: 'Hard (30 points)' }
              ]}
            />
          </div>
          
          <button
            on:click={startQuiz}
            disabled={loading}
            class="btn-primary w-full"
          >
            {loading ? 'Loading...' : '🚀 Start Quiz'}
          </button>
        </div>
      </div>
      
      <div class="card">
        <h3 class="text-2xl font-bold mb-6 text-white">🏆 Leaderboard</h3>
        
        {#if loadingLeaderboard && leaderboard.length === 0}
          <div class="space-y-3">
            {#each [1, 2, 3, 4, 5] as _}
              <SkeletonLoader height="60px" />
            {/each}
          </div>
        {:else if leaderboard.length === 0}
          <p class="text-gray-400 text-sm">No scores yet. Be the first!</p>
        {:else}
          <div class="space-y-3">
            {#each leaderboard as entry}
              <div class="flex items-center justify-between bg-white/5 border border-white/10 rounded-lg p-3 transition-all duration-150 hover:bg-white/[0.08]">
                <div class="flex items-center gap-3">
                  <div class="text-lg font-bold {entry.rank === 1 ? 'text-white' : entry.rank === 2 ? 'text-gray-300' : entry.rank === 3 ? 'text-gray-400' : 'text-gray-500'}">
                    #{entry.rank}
                  </div>
                  <div>
                    <div class="font-bold text-white text-sm">{entry.username}</div>
                    <div class="text-xs text-gray-400">
                      {formatTime(entry.time_taken)}
                    </div>
                  </div>
                </div>
                <div class="text-lg font-bold text-white">{entry.score}</div>
              </div>
            {/each}
          </div>
        {/if}
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
      <div class="card lg:col-span-2">
        <h2 class="text-2xl font-display font-bold text-white mb-6">How It Works</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <div class="flex items-center gap-2 mb-2">
              <div class="w-8 h-8 rounded-lg bg-white/[0.04] border border-white/[0.08] flex items-center justify-center">
                <span class="text-lg">🎯</span>
              </div>
              <h3 class="text-lg font-semibold text-white">Answer SQL Questions</h3>
            </div>
            <p class="text-sm text-white/60 ml-10">Write SQL queries to answer questions across 110 different challenges covering beginner to advanced topics.</p>
          </div>
          <div>
            <div class="flex items-center gap-2 mb-2">
              <div class="w-8 h-8 rounded-lg bg-white/[0.04] border border-white/[0.08] flex items-center justify-center">
                <span class="text-lg">⚡</span>
              </div>
              <h3 class="text-lg font-semibold text-white">Real-Time Validation</h3>
            </div>
            <p class="text-sm text-white/60 ml-10">Your queries are executed against a real PostgreSQL database and results are compared for instant feedback.</p>
          </div>
          <div>
            <div class="flex items-center gap-2 mb-2">
              <div class="w-8 h-8 rounded-lg bg-white/[0.04] border border-white/[0.08] flex items-center justify-center">
                <span class="text-lg">🏆</span>
              </div>
              <h3 class="text-lg font-semibold text-white">Compete on Leaderboard</h3>
            </div>
            <p class="text-sm text-white/60 ml-10">Your score and completion time are tracked in a Redis-powered leaderboard to compete with other players.</p>
          </div>
          <div>
            <div class="flex items-center gap-2 mb-2">
              <div class="w-8 h-8 rounded-lg bg-white/[0.04] border border-white/[0.08] flex items-center justify-center">
                <span class="text-lg">📊</span>
              </div>
              <h3 class="text-lg font-semibold text-white">Difficulty Levels</h3>
            </div>
            <p class="text-sm text-white/60 ml-10">Choose from Easy (10 pts), Medium (20 pts), or Hard (30 pts) questions, or mix all difficulties for varied challenge.</p>
          </div>
        </div>
      </div>

      <div class="card">
        <h2 class="text-2xl font-display font-bold text-white mb-6">SQL Topics Covered</h2>
        <div class="space-y-3">
          <div class="bg-white/[0.02] border border-white/[0.08] rounded-lg p-3">
            <h3 class="font-semibold text-white text-sm mb-1">Fundamentals</h3>
            <p class="text-xs text-white/60">SELECT, WHERE, ORDER BY, LIMIT, DISTINCT</p>
          </div>
          <div class="bg-white/[0.02] border border-white/[0.08] rounded-lg p-3">
            <h3 class="font-semibold text-white text-sm mb-1">Joins & Relations</h3>
            <p class="text-xs text-white/60">INNER JOIN, LEFT JOIN, CROSS JOIN, self-joins</p>
          </div>
          <div class="bg-white/[0.02] border border-white/[0.08] rounded-lg p-3">
            <h3 class="font-semibold text-white text-sm mb-1">Aggregations</h3>
            <p class="text-xs text-white/60">GROUP BY, COUNT, SUM, AVG, MIN, MAX, HAVING</p>
          </div>
          <div class="bg-white/[0.02] border border-white/[0.08] rounded-lg p-3">
            <h3 class="font-semibold text-white text-sm mb-1">Advanced</h3>
            <p class="text-xs text-white/60">Subqueries, date functions, CASE, window functions</p>
          </div>
        </div>
      </div>
    </div>

    <div class="card">
      <h2 class="text-2xl font-display font-bold text-white mb-4">Technical Implementation</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="bg-white/[0.02] border border-white/[0.08] rounded-lg p-4">
          <h3 class="font-semibold text-white mb-2">Frontend</h3>
          <ul class="text-sm text-white/60 space-y-1">
            <li>• Svelte reactive state management</li>
            <li>• Real-time timer and progress tracking</li>
            <li>• Dynamic quiz configuration (5-20 questions)</li>
            <li>• Instant feedback with expected queries</li>
          </ul>
        </div>
        <div class="bg-white/[0.02] border border-white/[0.08] rounded-lg p-4">
          <h3 class="font-semibold text-white mb-2">Backend</h3>
          <ul class="text-sm text-white/60 space-y-1">
            <li>• PostgreSQL query execution & validation</li>
            <li>• Redis sorted sets for leaderboard</li>
            <li>• Normalized result comparison algorithm</li>
            <li>• 110 hand-crafted SQL challenges</li>
          </ul>
        </div>
      </div>
    </div>
  {:else if quizStarted && !quizCompleted}
    <div class="mb-6 bg-white/5 border border-white/10 rounded-lg p-4">
      <div class="flex justify-between items-center mb-3">
        <div class="text-white">
          Question {currentQuestionIndex + 1} of {questions.length}
        </div>
        <div class="text-white">
          Score: <span class="font-bold">{score}</span> pts
        </div>
        <div class="text-white">
          Time: <span class="font-mono">{formatTime(elapsedTime)}</span>
        </div>
      </div>
      
      <div class="w-full bg-gray-800 rounded-full h-2">
        <div
          class="bg-gradient-to-r from-white to-gray-400 h-2 rounded-full transition-all duration-300"
          style="width: {progress}%"
        ></div>
      </div>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
      <div class="card">
          <div class="mb-6">
            <div class="flex items-center justify-between mb-4">
              <span class="badge">{currentQuestion.difficulty} • {currentQuestion.points} pts</span>
              <span class="text-sm text-gray-400">{currentQuestion.category}</span>
            </div>
            
            <h3 class="text-xl font-bold text-white mb-4">{currentQuestion.question}</h3>
            
            <div>
              <label for="query-editor" class="block text-sm font-medium mb-2">Your SQL Query</label>
              <textarea
                id="query-editor"
                bind:value={userQuery}
                placeholder="SELECT ..."
                class="w-full bg-gray-900 border border-white/20 rounded-lg px-4 py-3 font-mono text-sm h-40"
              ></textarea>
            </div>
          </div>
          
          <div class="space-y-3">
            <button
              on:click={submitAnswer}
              disabled={loading || !userQuery.trim()}
              class="btn-primary w-full"
            >
              {loading ? 'Checking...' : '✓ Submit Answer'}
            </button>
            
            {#if feedback}
              <div class="p-4 rounded-lg {feedback.includes('Correct') ? 'bg-white/10 border border-white/30' : 'bg-gray-800 border border-gray-600'}">
                <p class="{feedback.includes('Correct') ? 'text-white' : 'text-gray-300'}">{feedback}</p>
                
                {#if showAnswer && expectedQuery}
                  <div class="mt-3">
                    <div class="text-sm font-medium mb-2 text-gray-400">Expected Query:</div>
                    <pre class="bg-gray-900 p-3 rounded text-sm text-gray-300 overflow-auto">{expectedQuery}</pre>
                  </div>
                {/if}
              </div>
            {/if}
            
            {#if feedback}
              <button
                on:click={nextQuestion}
                class="btn-secondary w-full"
              >
                {currentQuestionIndex < questions.length - 1 ? '→ Next Question' : '🏁 Finish Quiz'}
              </button>
            {/if}
          </div>
      </div>
      
      <div class="card">
        <h3 class="text-2xl font-bold mb-6 text-white">🏆 Leaderboard</h3>
        
        {#if loadingLeaderboard && leaderboard.length === 0}
          <div class="space-y-3">
            {#each [1, 2, 3, 4, 5] as _}
              <SkeletonLoader height="60px" />
            {/each}
          </div>
        {:else if leaderboard.length === 0}
          <p class="text-gray-400 text-sm">No scores yet. Be the first!</p>
        {:else}
          <div class="space-y-3">
            {#each leaderboard as entry}
              <div class="flex items-center justify-between bg-white/5 border border-white/10 rounded-lg p-3 transition-all duration-150 hover:bg-white/[0.08]">
                <div class="flex items-center gap-3">
                  <div class="text-lg font-bold {entry.rank === 1 ? 'text-white' : entry.rank === 2 ? 'text-gray-300' : entry.rank === 3 ? 'text-gray-400' : 'text-gray-500'}">
                    #{entry.rank}
                  </div>
                  <div>
                    <div class="font-bold text-white text-sm">{entry.username}</div>
                    <div class="text-xs text-gray-400">
                      {formatTime(entry.time_taken)}
                    </div>
                  </div>
                </div>
                <div class="text-lg font-bold text-white">{entry.score}</div>
              </div>
            {/each}
          </div>
        {/if}
      </div>
    </div>
  {:else if quizCompleted}
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
      <div class="card text-center">
        <h2 class="text-3xl font-bold mb-4 text-white">🎉 Quiz Complete!</h2>
        
        <div class="mb-8">
          <div class="text-5xl font-bold text-white mb-2">{score}</div>
          <div class="text-gray-400">Total Points</div>
          
          <div class="mt-6 flex justify-center gap-8">
            <div>
              <div class="text-2xl font-bold text-white">{questions.length}</div>
              <div class="text-sm text-gray-400">Questions</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-white">{formatTime(elapsedTime)}</div>
              <div class="text-sm text-gray-400">Time</div>
            </div>
            {#if userStats.rank}
              <div>
                <div class="text-2xl font-bold text-white">#{userStats.rank}</div>
                <div class="text-sm text-gray-400">Rank</div>
              </div>
            {/if}
          </div>
        </div>
        
        <button on:click={restartQuiz} class="btn-primary w-full">
          🔄 Take Another Quiz
        </button>
      </div>
      
      <div class="card">
        <h3 class="text-2xl font-bold mb-6 text-white">🏆 Leaderboard</h3>
        
        {#if loadingLeaderboard && leaderboard.length === 0}
          <div class="space-y-3">
            {#each [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] as _}
              <SkeletonLoader height="60px" />
            {/each}
          </div>
        {:else if leaderboard.length === 0}
          <p class="text-gray-400">No scores yet. Be the first to complete the quiz!</p>
        {:else}
          <div class="space-y-3">
            {#each leaderboard as entry}
              <div class="flex items-center justify-between bg-white/5 border border-white/10 rounded-lg p-4 {entry.username.toLowerCase() === username.toLowerCase() ? 'ring-2 ring-white/30' : ''}">
                <div class="flex items-center gap-4">
                  <div class="text-2xl font-bold {entry.rank === 1 ? 'text-white' : entry.rank === 2 ? 'text-gray-300' : entry.rank === 3 ? 'text-gray-400' : 'text-gray-500'}">
                    #{entry.rank}
                  </div>
                  <div>
                    <div class="font-bold text-white">
                      {entry.username}
                      {#if entry.username.toLowerCase() === username.toLowerCase()}
                        <span class="text-sm text-gray-400">(You)</span>
                      {/if}
                    </div>
                    <div class="text-sm text-gray-400">
                      {formatTime(entry.time_taken)}
                    </div>
                  </div>
                </div>
                <div class="text-xl font-bold text-white">{entry.score} pts</div>
              </div>
            {/each}
          </div>
        {/if}
      </div>
    </div>
  {/if}
  </div>
</div>

<Footer />
