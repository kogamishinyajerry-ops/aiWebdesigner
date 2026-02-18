'use client'

import { useState, useEffect } from 'react'

export default function TestConnectionPage() {
  const [results, setResults] = useState<{[key: string]: string}>({})

  useEffect(() => {
    async function testConnections() {
      const tests = {
        'Frontend': 'Frontend is working!',
        'Backend Health': `${process.env.NEXT_PUBLIC_API_URL}/health`,
        'Backend Docs': `${process.env.NEXT_PUBLIC_API_URL}/docs`,
        'Current URL': window.location.href,
        'API URL': process.env.NEXT_PUBLIC_API_URL || 'Not set',
      }

      const results: {[key: string]: string} = {}
      results['Frontend'] = '✅ Frontend page loaded successfully'
      results['Current URL'] = window.location.href
      results['API URL Config'] = process.env.NEXT_PUBLIC_API_URL || 'Not configured'

      // Test backend
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/health`)
        if (response.ok) {
          const data = await response.json()
          results['Backend Health'] = `✅ ${JSON.stringify(data)}`
        } else {
          results['Backend Health'] = `❌ HTTP ${response.status}`
        }
      } catch (error) {
        results['Backend Health'] = `❌ Connection failed: ${error}`
      }

      setResults(results)
    }

    testConnections()
  }, [])

  return (
    <div className="min-h-screen bg-background p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Cloud Studio 连接测试</h1>

        <div className="space-y-4">
          <div className="bg-muted p-4 rounded-lg">
            <h2 className="text-xl font-semibold mb-4">测试结果</h2>
            <div className="space-y-3">
              {Object.entries(results).map(([key, value]) => (
                <div key={key} className="border-b pb-2">
                  <div className="font-medium">{key}</div>
                  <div className="text-sm text-muted-foreground mt-1">{value}</div>
                </div>
              ))}
              {Object.keys(results).length === 0 && (
                <div className="text-muted-foreground">正在测试连接...</div>
              )}
            </div>
          </div>

          <div className="bg-muted p-4 rounded-lg">
            <h2 className="text-xl font-semibold mb-4">手动测试</h2>
            <div className="space-y-2">
              <a
                href="/"
                className="block text-blue-500 hover:underline"
              >
                → 返回首页
              </a>
              <a
                href="/generator/image"
                className="block text-blue-500 hover:underline"
              >
                → 图像生成器
              </a>
              <a
                href="/dashboard"
                className="block text-blue-500 hover:underline"
              >
                → Dashboard
              </a>
            </div>
          </div>

          <div className="bg-yellow-50 dark:bg-yellow-900/20 p-4 rounded-lg">
            <h2 className="text-xl font-semibold mb-2">使用说明</h2>
            <ol className="list-decimal list-inside space-y-2 text-sm">
              <li>检查上面的测试结果</li>
              <li>如果 Backend Health 测试失败，请确保后端服务（8000端口）正在运行</li>
              <li>确保在 Cloud Studio 中同时暴露了 3000 和 8000 端口</li>
              <li>查看 <code>/workspace/ai_designer/CLOUD_STUDIO_ACCESS.md</code> 获取详细帮助</li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  )
}
