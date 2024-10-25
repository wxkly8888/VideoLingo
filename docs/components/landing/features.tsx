import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { CheckCircle, ArrowRight } from 'lucide-react'

// 定义Feature类型
type Feature = {
	title: string
	description: string
	icon: 'CheckCircle' | 'ArrowRight'
}

// 定义组件props类型
type FeaturesProps = {
	features: Feature[]
	title: string
}

// 修改组件为接受props的形式
export default function Features({ features, title }: FeaturesProps) {
	// 创建图标映射
	const iconMap = {
		CheckCircle: <CheckCircle className="h-10 w-10 text-primary" />,
		ArrowRight: <ArrowRight className="h-10 w-10 text-primary" />,
	}

	return (
		<section id="features" className="w-full py-24 md:py-32">
			<div className="container mx-auto px-4 md:px-6">
				<h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl text-center mb-16">
					{title}
				</h2>
				<div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
					{features.map((feature, index) => (
						<Card key={index} className="n-card">
							<CardHeader>
								<div className="flex items-center space-x-4">
									{iconMap[feature.icon]}
									<CardTitle>{feature.title}</CardTitle>
								</div>
							</CardHeader>
							<CardContent>
								<p>{feature.description}</p>
							</CardContent>
						</Card>
					))}
				</div>
			</div>
		</section>
	)
}
