'use client'

import { useState, useCallback } from 'react'
import ReactFlow, {
  Node,
  Edge,
  addEdge,
  Background,
  Controls,
  MiniMap,
  Connection,
  useNodesState,
  useEdgesState,
} from 'reactflow'
import 'reactflow/dist/style.css'

const initialNodes: Node[] = [
  {
    id: '1',
    type: 'input',
    data: { label: 'Agent Blueprint' },
    position: { x: 250, y: 25 },
  },
]

const initialEdges: Edge[] = []

export default function AgentBuilder() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes)
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges)
  const [selectedStrategy, setSelectedStrategy] = useState('alpha-coder')

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  )

  const addNode = (type: string) => {
    const newNode: Node = {
      id: `${nodes.length + 1}`,
      type: 'default',
      data: { label: type },
      position: { x: Math.random() * 400, y: Math.random() * 400 },
    }
    setNodes((nds) => nds.concat(newNode))
  }

  return (
    <div className="h-screen flex flex-col">
      {/* Header */}
      <div className="bg-white shadow-sm p-4 flex justify-between items-center">
        <h1 className="text-2xl font-bold text-primary-600">Agent Builder</h1>
        <div className="flex space-x-4">
          <button className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300">
            Save Draft
          </button>
          <button className="px-4 py-2 bg-primary-600 text-white rounded hover:bg-primary-700">
            Start Evolution
          </button>
        </div>
      </div>

      <div className="flex-1 flex">
        {/* Left Sidebar - Component Library */}
        <div className="w-64 bg-white shadow-md p-4 overflow-y-auto">
          <h2 className="text-lg font-bold mb-4">Components</h2>

          <div className="space-y-2">
            <button
              onClick={() => addNode('Role Node')}
              className="w-full px-4 py-2 bg-blue-100 rounded hover:bg-blue-200 text-left"
            >
              📝 Role Node
            </button>
            <button
              onClick={() => addNode('Model Node')}
              className="w-full px-4 py-2 bg-purple-100 rounded hover:bg-purple-200 text-left"
            >
              🤖 Model Node
            </button>
            <button
              onClick={() => addNode('Memory Node')}
              className="w-full px-4 py-2 bg-green-100 rounded hover:bg-green-200 text-left"
            >
              🧠 Memory Node
            </button>
            <button
              onClick={() => addNode('Environment Node')}
              className="w-full px-4 py-2 bg-yellow-100 rounded hover:bg-yellow-200 text-left"
            >
              🏗️ Environment Node
            </button>
          </div>

          <hr className="my-6" />

          <h2 className="text-lg font-bold mb-4">Evolution Strategy</h2>

          <select
            value={selectedStrategy}
            onChange={(e) => setSelectedStrategy(e.target.value)}
            className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="alpha-coder">Alpha-Coder Loop</option>
            <option value="curiosity">Curiosity Loop</option>
            <option value="adversarial">Adversarial Arena</option>
          </select>

          <div className="mt-4 p-3 bg-gray-50 rounded text-sm">
            {selectedStrategy === 'alpha-coder' && (
              <div>
                <p className="font-semibold mb-2">Alpha-Coder Loop</p>
                <p className="text-gray-600">
                  Optimizes code through mutation and selection. Best for algorithmic tasks.
                </p>
              </div>
            )}
            {selectedStrategy === 'curiosity' && (
              <div>
                <p className="font-semibold mb-2">Curiosity Loop</p>
                <p className="text-gray-600">
                  Generates synthetic tasks and learns from experience. Best for exploration.
                </p>
              </div>
            )}
            {selectedStrategy === 'adversarial' && (
              <div>
                <p className="font-semibold mb-2">Adversarial Arena</p>
                <p className="text-gray-600">
                  Three agents co-evolve. Best for complex reasoning and math.
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Canvas */}
        <div className="flex-1">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            fitView
          >
            <Background />
            <Controls />
            <MiniMap />
          </ReactFlow>
        </div>

        {/* Right Sidebar - Properties */}
        <div className="w-80 bg-white shadow-md p-4 overflow-y-auto">
          <h2 className="text-lg font-bold mb-4">Properties</h2>
          <p className="text-gray-500 text-sm">
            Select a node to edit its properties
          </p>

          <div className="mt-6 space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Max Generations</label>
              <input
                type="number"
                defaultValue={100}
                className="w-full px-3 py-2 border rounded"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Population Size</label>
              <input
                type="number"
                defaultValue={50}
                className="w-full px-3 py-2 border rounded"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Mutation Rate</label>
              <input
                type="range"
                min="0"
                max="1"
                step="0.1"
                defaultValue="0.3"
                className="w-full"
              />
              <span className="text-sm text-gray-600">0.3</span>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Judge Type</label>
              <select className="w-full px-3 py-2 border rounded">
                <option>Rule-Based</option>
                <option>LLM Judge</option>
                <option>Evolving Judge</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
