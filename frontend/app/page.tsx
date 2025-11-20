'use client'

import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen">
      {/* Header */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-primary-600">EvoForge</h1>
            </div>
            <div className="flex space-x-4">
              <Link href="/builder" className="text-gray-700 hover:text-primary-600">
                Builder
              </Link>
              <Link href="/agents" className="text-gray-700 hover:text-primary-600">
                Agents
              </Link>
              <Link href="/dashboard" className="text-gray-700 hover:text-primary-600">
                Dashboard
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center">
          <h1 className="text-5xl font-extrabold text-gray-900 mb-6">
            From Static Prompts to <span className="text-primary-600">Living Intelligence</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            EvoForge transforms AI agents from frozen artifacts into self-evolving systems.
            Define the constraints, and watch your agents improve autonomously through
            evolutionary algorithms inspired by cutting-edge research.
          </p>
          <div className="flex justify-center space-x-4">
            <Link
              href="/builder"
              className="px-8 py-3 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 transition"
            >
              Start Building
            </Link>
            <Link
              href="/docs"
              className="px-8 py-3 bg-white text-primary-600 border-2 border-primary-600 rounded-lg font-semibold hover:bg-primary-50 transition"
            >
              Documentation
            </Link>
          </div>
        </div>

        {/* Features */}
        <div className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-3xl mb-4">🧬</div>
            <h3 className="text-xl font-bold mb-2">AlphaEvolve</h3>
            <p className="text-gray-600">
              Optimize code and algorithms through mutation and natural selection.
              Your agents rewrite their own logic to find better solutions.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-3xl mb-4">🎯</div>
            <h3 className="text-xl font-bold mb-2">Self-Questioning</h3>
            <p className="text-gray-600">
              Generate synthetic training data automatically. Start with 5 examples,
              get thousands through intelligent curriculum generation.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-3xl mb-4">⚡</div>
            <h3 className="text-xl font-bold mb-2">Co-Evolution</h3>
            <p className="text-gray-600">
              Three agents work together: Proposer creates challenges, Solver attempts them,
              Judge evaluates. All improve simultaneously.
            </p>
          </div>
        </div>

        {/* Evolution Layers */}
        <div className="mt-20">
          <h2 className="text-3xl font-bold text-center mb-12">Three Layers of Evolution</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-8 rounded-lg">
              <h3 className="text-2xl font-bold mb-4">1. Prompt Evolution</h3>
              <p className="text-gray-700 mb-4">
                Optimize system instructions and few-shot examples based on feedback.
              </p>
              <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                <li>Experience Pool retrieval</li>
                <li>Dynamic example injection</li>
                <li>Meta-optimizer rewrites</li>
              </ul>
              <div className="mt-4 text-sm">
                <span className="font-semibold">Cost:</span> Low |
                <span className="font-semibold"> Speed:</span> Fast
              </div>
            </div>

            <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-8 rounded-lg">
              <h3 className="text-2xl font-bold mb-4">2. Code Evolution</h3>
              <p className="text-gray-700 mb-4">
                Rewrite Python functions and create new tools on the fly.
              </p>
              <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                <li>Heuristic discovery</li>
                <li>Algorithm optimization</li>
                <li>Sandboxed validation</li>
              </ul>
              <div className="mt-4 text-sm">
                <span className="font-semibold">Cost:</span> Medium |
                <span className="font-semibold"> Speed:</span> Medium
              </div>
            </div>

            <div className="bg-gradient-to-br from-green-50 to-green-100 p-8 rounded-lg">
              <h3 className="text-2xl font-bold mb-4">3. Model Evolution</h3>
              <p className="text-gray-700 mb-4">
                Fine-tune LLM weights through reinforcement learning.
              </p>
              <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                <li>Task-Relative REINFORCE++</li>
                <li>LoRA adapters</li>
                <li>Process-based attribution</li>
              </ul>
              <div className="mt-4 text-sm">
                <span className="font-semibold">Cost:</span> High |
                <span className="font-semibold"> Speed:</span> Slow
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}
