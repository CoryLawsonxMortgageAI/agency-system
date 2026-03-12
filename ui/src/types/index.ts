export interface AgentConfig {
  id: string;
  name: string;
  division: string;
  personality: {
    name: string;
    role: string;
    tone: string;
    catchphrase?: string;
    communication_style: string;
    expertise_areas: string[];
  };
  capabilities: {
    name: string;
    description: string;
    skills: string[];
    tools: string[];
  };
  system_prompt: string;
  model: string;
  temperature: number;
  max_tokens: number;
  active: boolean;
  metadata?: Record<string, any>;
}

export interface AgentStatus {
  agent_id: string;
  status: 'idle' | 'active' | 'busy' | 'error' | 'offline';
  current_task?: string;
  queue_depth: number;
  total_tasks_completed: number;
  total_tasks_failed: number;
  average_response_time: number;
  last_active?: string;
  metrics?: Record<string, any>;
}

export interface SystemStatus {
  status: string;
  uptime: number;
  active_agents: number;
  total_agents: number;
  active_workflows: number;
  queue_depth: number;
  metrics: {
    cpu_usage: number;
    memory_usage: number;
    active_connections: number;
    requests_per_second: number;
    average_response_time: number;
    error_rate: number;
  };
  timestamp: string;
}

export interface TaskRequest {
  agent_id: string;
  task_data: {
    instruction: string;
    input?: Record<string, any>;
    requirements?: string;
    expected_output?: string;
  };
  context?: Record<string, any>;
  priority?: number;
  timeout?: number;
}

export interface TaskResult {
  task_id: string;
  agent_id: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';
  output: any;
  error?: string;
  execution_time: number;
  tokens_used?: number;
  cost?: number;
  created_at: string;
  completed_at?: string;
}

export interface WorkflowStep {
  id: string;
  name: string;
  agent_id: string;
  task_template: Record<string, any>;
  dependencies: string[];
  condition?: string;
  retry_count: number;
  timeout: number;
}

export interface WorkflowDefinition {
  id?: string;
  name: string;
  description: string;
  steps: WorkflowStep[];
  parallel_groups: string[][];
  input_schema?: Record<string, any>;
  output_schema?: Record<string, any>;
  timeout?: number;
  auto_retry?: boolean;
  created_by?: string;
  tags?: string[];
}

export interface WorkflowExecution {
  execution_id: string;
  workflow_id: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'paused';
  input_data: Record<string, any>;
  step_results: Record<string, TaskResult>;
  current_step?: string;
  progress_percentage: number;
  started_at: string;
  completed_at?: string;
  error_message?: string;
}

export interface AutonomousConfig {
  enabled: boolean;
  scan_interval: number;
  max_concurrent_tasks: number;
  scaling_threshold: number;
  auto_discover_tasks: boolean;
  task_sources: string[];
  notification_channels: string[];
  learning_enabled: boolean;
}

export const DIVISION_COLORS: Record<string, string> = {
  Engineering: 'bg-engineering text-white',
  Marketing: 'bg-marketing text-white',
  Product: 'bg-product text-white',
  Testing: 'bg-testing text-black',
  Support: 'bg-support text-white',
  Specialized: 'bg-specialized text-white',
};

export const STATUS_COLORS: Record<string, string> = {
  idle: 'bg-slate-500',
  active: 'bg-green-500',
  busy: 'bg-blue-500',
  error: 'bg-red-500',
  offline: 'bg-gray-500',
};
