import { useState, useRef, useEffect } from 'react';
import { 
  Terminal, 
  Send, 
  Trash2, 
  Download,
  ChevronRight
} from 'lucide-react';
import { cn } from '@/lib/utils';

interface LogEntry {
  id: string;
  timestamp: string;
  level: 'info' | 'warning' | 'error' | 'success';
  agent?: string;
  message: string;
}

const SAMPLE_LOGS: LogEntry[] = [
  { id: '1', timestamp: '12:34:56', level: 'success', agent: 'frontend-developer', message: 'Task completed: Built React component' },
  { id: '2', timestamp: '12:34:52', level: 'info', agent: 'content-creator', message: 'Starting content generation workflow' },
  { id: '3', timestamp: '12:34:48', level: 'info', message: 'Autonomous mode: Queue depth within normal range' },
  { id: '4', timestamp: '12:34:45', level: 'warning', agent: 'backend-architect', message: 'High latency detected in API calls' },
  { id: '5', timestamp: '12:34:42', level: 'success', agent: 'growth-hacker', message: 'A/B test results: 23% improvement' },
  { id: '6', timestamp: '12:34:38', level: 'info', agent: 'seo-specialist', message: 'Crawling sitemap...' },
  { id: '7', timestamp: '12:34:35', level: 'error', agent: 'devops-automator', message: 'Deployment failed: Timeout exceeded' },
  { id: '8', timestamp: '12:34:32', level: 'success', message: 'System health check passed' },
  { id: '9', timestamp: '12:34:28', level: 'info', agent: 'ai-engineer', message: 'Model inference: 2.3s response time' },
  { id: '10', timestamp: '12:34:25', level: 'success', agent: 'analytics-reporter', message: 'Daily report generated' },
];

export function TerminalPanel() {
  const [logs, setLogs] = useState<LogEntry[]>(SAMPLE_LOGS);
  const [input, setInput] = useState('');
  const [filter, setFilter] = useState<'all' | 'info' | 'warning' | 'error'>('all');
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  const handleSend = () => {
    if (!input.trim()) return;
    
    const newLog: LogEntry = {
      id: Date.now().toString(),
      timestamp: new Date().toLocaleTimeString(),
      level: 'info',
      message: `Command executed: ${input}`,
    };
    
    setLogs([...logs, newLog]);
    setInput('');
  };

  const filteredLogs = filter === 'all' 
    ? logs 
    : logs.filter(log => log.level === filter || (filter === 'error' && log.level === 'warning'));

  const levelColors = {
    info: 'text-blue-400',
    warning: 'text-yellow-400',
    error: 'text-red-400',
    success: 'text-green-400'
  };

  const levelBgColors = {
    info: 'bg-blue-500/10',
    warning: 'bg-yellow-500/10',
    error: 'bg-red-500/10',
    success: 'bg-green-500/10'
  };

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <Terminal className="w-6 h-6 text-primary" />
          <div>
            <h2 className="text-xl font-bold">Command Terminal</h2>
            <p className="text-sm text-muted-foreground">Execute commands and monitor system logs</p>
          </div>
        </div>
        
        <div className="flex items-center gap-2">
          <button 
            onClick={() => setLogs([])}
            className="flex items-center gap-2 px-3 py-2 text-sm hover:bg-accent rounded-lg transition-colors"
          >
            <Trash2 className="w-4 h-4" />
            Clear
          </button>
          <button className="flex items-center gap-2 px-3 py-2 text-sm hover:bg-accent rounded-lg transition-colors">
            <Download className="w-4 h-4" />
            Export
          </button>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center gap-2 mb-4">
        {(['all', 'info', 'warning', 'error'] as const).map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={cn(
              "px-4 py-2 rounded-lg text-sm font-medium transition-colors capitalize",
              filter === f 
                ? "bg-primary text-primary-foreground" 
                : "bg-card border border-border hover:bg-accent"
            )}
          >
            {f}
            {f !== 'all' && (
              <span className="ml-2 text-xs opacity-70">
                {logs.filter(l => l.level === f).length}
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Terminal Output */}
      <div 
        ref={scrollRef}
        className="flex-1 bg-black/90 rounded-xl border border-border p-4 font-mono text-sm overflow-y-auto"
      >
        <div className="space-y-2">
          {filteredLogs.map((log) => (
            <div 
              key={log.id}
              className={cn(
                "flex items-start gap-3 p-2 rounded",
                levelBgColors[log.level]
              )}
            >
              <span className="text-muted-foreground text-xs shrink-0 w-16">
                {log.timestamp}
              </span>
              <span className={cn(
                "text-xs uppercase font-bold shrink-0 w-16",
                levelColors[log.level]
              )}>
                {log.level}
              </span>
              {log.agent && (
                <span className="text-purple-400 text-xs shrink-0">
                  [{log.agent}]
                </span>
              )}
              <span className="text-foreground/90">{log.message}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Input */}
      <div className="mt-4 flex items-center gap-3">
        <div className="flex-1 flex items-center gap-3 px-4 py-3 bg-card border border-border rounded-xl">
          <ChevronRight className="w-5 h-5 text-primary" />
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Enter command (e.g., 'agents list', 'execute frontend-developer')..."
            className="flex-1 bg-transparent outline-none text-sm"
          />
        </div>
        <button
          onClick={handleSend}
          className="p-3 bg-primary text-primary-foreground rounded-xl hover:bg-primary/90 transition-colors"
        >
          <Send className="w-5 h-5" />
        </button>
      </div>

      {/* Quick Commands */}
      <div className="mt-4 flex items-center gap-2 flex-wrap">
        <span className="text-xs text-muted-foreground">Quick commands:</span>
        {['agents list', 'status', 'autonomous start', 'workflow run marketing', 'help'].map(cmd => (
          <button
            key={cmd}
            onClick={() => setInput(cmd)}
            className="px-2 py-1 text-xs bg-accent hover:bg-accent/80 rounded transition-colors"
          >
            {cmd}
          </button>
        ))}
      </div>
    </div>
  );
}
