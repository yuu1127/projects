import java.io.Serializable;
import java.util.ArrayList;
import java.util.Iterator;

import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.api.java.function.PairFlatMapFunction;
import org.apache.spark.api.java.function.PairFunction;

import scala.Tuple2;

/*Documentation and code structure

As we know there are many solutions for the shortest path program such as Dijkstra’s algorithm, however in this situation we need to solve this program using spark(map-reduce process).
Therefore, the efficient way might be using parallel breadth first search which matches map-reduce process using RDD.
The first thing we need to do is making adjacency lists for this graph program, then I made AdjList class for this. The structure is below
Key: (node name), Value: (distance + status + path + lstnodes(iterable tuple2<adjacent nodes,weight>)).
I initiated distance value to 10000 except original node which is provided by input arguments (its distance is 0).
Next important step is iterating map-reduce passes.I used do-while loop and put map-reduce process (flatMapToPair,groupByKey) inside loop,
in addition I made next nodes array-lists so that helps to indicates which nodes we need to move from current nodes for next iteration.
For mapper, it emits distance value, in detail for each RDD iteration it checks the next nodes list if it include the node,
it emits new AdjLIst whose distance is the node distance + weight for its each adjacent nodes( this lstnodes is null
since it needs only distance to compare and lstnodes would inherit by original node in reduce stage).
In reducer stage (groupByKey.flatMapToPair(MinValue)), it selects minimum distance path for each reachable node with status and path values and inherits lstnodes from original old AdjList.
Another note is when we terminate iterations. For my data structure, it has status value and if it has passed every node except unreachable it terminates loops.
In the worst case, N iteration need, so in case my program stops if the number of iterations is more than N + 5.
Finally, it sorts by distance using mapper and save output in part-0000.txt.

 */

public class AssigTwoz5186797 {
	public static String OriginNode = "";
	public static String NextNode = "";
	public static ArrayList<String> NextNodes = new ArrayList<String>();
	public static ArrayList<String> SaveNodes = new ArrayList<String>();


	// Minvalue using after reducer to select min ditance and inherit lstnodes
	private static class MinValue implements PairFlatMapFunction<Tuple2<String,Iterable<AdjList>>, String, AdjList>{
		@Override
		public Iterator<Tuple2<String, AdjList>> call(Tuple2<String, Iterable<AdjList>> input) throws Exception{
			String fromnode = input._1;
			Iterable<AdjList> adjs = input._2;
			ArrayList<Tuple2<String,AdjList>> ret = new ArrayList<Tuple2<String,AdjList>>();
			Iterable<Tuple2<String, Integer>> lstNodes1 = null;
			Integer min_distance = 10000;
			Integer status = 0;
			AdjList adj1 = new AdjList(min_distance, lstNodes1);
			//String new_path = "";
			//Iterable<Tuple2<String, Integer>> lstNodes = adj.lstNodes;
			for(AdjList s : adjs){
				   //Do whatever you want
				//System.out.println("HAAAAAAA");
				if(s.distance < min_distance) {
					min_distance = s.distance;
					status = s.status;
					adj1.path = s.path;
				}
				if(s.lstNodes != null) {
					adj1.lstNodes = s.lstNodes;
				}
			}
			//AdjList adj1 = new AdjList(min_distance, lstNodes);
			adj1.distance = min_distance;
			adj1.status = status;
			ret.add(new Tuple2<>(fromnode,adj1));
			return ret.iterator();
		}
	}

	// AdjList class for graph program Key: (node name), Value: (distance + status + path + lstnodes(iterable tuple2<adjacent nodes,weight>))
	public static class AdjList implements Serializable {
		Integer distance;
		Integer status = 0;
		Iterable<Tuple2<String, Integer>> lstNodes;
		String path = "";
		//Iterable ArrayList List;
		public AdjList(Integer distance,Iterable<Tuple2<String, Integer>> ListVal) {
			this.distance = distance;
			this.lstNodes =  ListVal;
		}
		public String toString() {
			StringBuilder sb = new StringBuilder();
			sb.append(distance).append(',').append(status).append(',').append(path).append(',').append(lstNodes);
			return sb.toString();
		}
		public Iterable<Tuple2<String, Integer>> get_nodes(){
			return this.lstNodes;
		}
	}

	public static void main(String[] args) {
		SparkConf conf = new SparkConf()
				.setAppName("Assignment 1")
				.setMaster("local");
		JavaSparkContext context = new JavaSparkContext(conf);
		// RDD[String]
		JavaRDD<String> input = context.textFile(args[1]);
		//System.out.println(input);

		// step1 make movie,rating tuple for each user
		// make dest,dist tuple for each node
		JavaPairRDD<String, Tuple2<String,Integer>> step1 = input.mapToPair(
				new PairFunction<String, String, Tuple2<String, Integer>>() {
					@Override
					public Tuple2<String, Tuple2<String, Integer>> call(String s) throws Exception {
						String[] aux = s.split(",");
						String fromNode = aux[0];
						String toNode = aux[1];
						Integer weight = Integer.parseInt(aux[2]);
						return new Tuple2<String, Tuple2<String,Integer>>(fromNode, new Tuple2<>(toNode, weight));
					}
		});

		JavaPairRDD<String, Iterable<Tuple2<String, Integer>>> step2 =  step1.groupByKey();

		//step2.saveAsTextFile(args[2]);
		// TODO add distance value
		//System.out.println(step2);
		//step2.saveAsTextFile(args[2]);

		//initialize distance value
		JavaPairRDD<String, AdjList> step3 = step2.mapToPair(
				new PairFunction<Tuple2<String, Iterable<Tuple2<String, Integer>>>, String, AdjList>() {
					@Override
					public Tuple2<String, AdjList> call(Tuple2<String, Iterable<Tuple2<String, Integer>>> input) throws Exception {
						Integer distance;
						String fromNode = input._1;
						if(fromNode.equals(args[0])) {
							distance = 0;
						}
						else {
							distance = 10000;
						}
						Iterable<Tuple2<String, Integer>> lstNodes = input._2;

						AdjList adj = new AdjList(distance, lstNodes);

						return new Tuple2<String, AdjList>(fromNode, adj);
					}
		});

		//step3.saveAsTextFile(args[2]);

		boolean hasEnded = true;
		boolean some_where = true;
		int i = 0;
		long max_ite = step3.count();
		//TODO: think about unreable we can stop ? and comment

		AssigTwoz5186797.OriginNode = args[0];
		//AssigTwoz5186797.NextNode = OriginNode;

		// RDD iteration mapping -> reduce -> mapping -> reduce ...
		// parallel breadth first search
		AssigTwoz5186797.SaveNodes.add(OriginNode);
		do {

			AssigTwoz5186797.NextNodes = new ArrayList<String>();
			for(String node: AssigTwoz5186797.SaveNodes) {
				AssigTwoz5186797.NextNodes.add(node);
			}

			AssigTwoz5186797.SaveNodes = new ArrayList<String>();
			step3 = step3.flatMapToPair(
				new PairFlatMapFunction<Tuple2<String, AdjList>, String, AdjList>() {
					@Override
					public Iterator<Tuple2<String, AdjList>> call(Tuple2<String, AdjList> input) throws Exception {

						ArrayList<Tuple2<String,AdjList>> ret = new ArrayList<Tuple2<String,AdjList>>();

						String from_Node = input._1;
						AdjList adj = input._2;
						Integer node_flag = 0;

						for(String node: AssigTwoz5186797.NextNodes) {
							if(from_Node.equals(node) && adj.lstNodes != null) {
								node_flag = 1;
							}
						}

						Iterable<Tuple2<String, Integer>> lstNodes = adj.lstNodes;
						if(node_flag == 1) {
							adj.status = 1;
							AssigTwoz5186797.SaveNodes.remove(from_Node);
							for(Tuple2<String, Integer> s : lstNodes){
								Integer new_distance = s._2 + adj.distance;
								Iterable<Tuple2<String, Integer>> lstNodes1 = null;
								AdjList adj1 = new AdjList(new_distance, lstNodes1);
								if(adj.path == "") {
									adj1.path = from_Node;
								}
								else {
									adj1.path = adj.path + "-" + from_Node;
								}
								AssigTwoz5186797.SaveNodes.add(s._1);
								ret.add(new Tuple2<>(s._1,adj1));
								//AssigTwoz5186797.NextNodes.add(s._1);
							}
						}
						//System.out.println(AssigTwoz5186797.NextNodes);
						//System.out.println(AssigTwoz5186797.SaveNodes);
						ret.add(new Tuple2<>(from_Node,adj));
						return ret.iterator();
				}
				//TODO:add next nodes outside of iteration
			}).groupByKey().flatMapToPair(new MinValue());

			hasEnded = false;
			some_where = false;
			for (Tuple2<String, AdjList> tuple : step3.collect()) {
				AdjList adj = tuple._2;
				//System.out.print(tuple._1 + " ");
				//System.out.println(adj);
				if(adj.status == 0 && adj.lstNodes != null) {
					hasEnded = true;
				}
				if(adj.status == 1) {
					some_where = true;
				}
			}
			if(some_where == false) {
				hasEnded = false;
			}
			i = i + 1;
			//System.out.print(i);
			//System.out.println("回目でーす");
			//System.out.println(max_ite);
			if(i > max_ite + 5) {
				hasEnded = false;
			}
			//break;
		} while (hasEnded);
		//System.out.println("処理が終了しました");

// TODO: after sortby -1 for unreachable
// sort by distance need iterate since no need start value

		// swip key(distance) ,value others for using sortByKey (in Java no sort by vakue)
		JavaPairRDD<Integer, String> step4 = step3.flatMapToPair(
				new PairFlatMapFunction<Tuple2<String, AdjList>, Integer, String>() {
					@Override
					public Iterator<Tuple2<Integer, String>> call(Tuple2<String, AdjList> input) throws Exception {
						ArrayList<Tuple2<Integer,String>> ret = new ArrayList<Tuple2<Integer,String>>();
						AdjList adj = input._2;
						//String key = String.valueOf(adj.distance);
						Integer key = adj.distance;
						//System.out.println(key);
						String value = "";
						String from_node = input._1;
						String path = adj.path + "-" + from_node;
						value = from_node + "," + path;
						if(!from_node.equals(AssigTwoz5186797.OriginNode)) {
							ret.add(new Tuple2<>(key,value));
						}
						return ret.iterator();
						//return new Tuple2<String, String>(key, value);
					}
		});

		step4 = step4.sortByKey();

//		step4.foreach(item -> {
//		System.out.println(item);
//		});

		//TODO:unreachable print -1 for 10000
		// change RDD output folloede by format
		JavaPairRDD<String, String> step5 = step4.mapToPair(
				new PairFunction<Tuple2<Integer, String>, String, String>() {
					@Override
					public Tuple2<String, String> call(Tuple2<Integer, String> input) throws Exception {
						Integer distance = input._1;
						String [] parts = input._2.split(",");
						String key = parts[0];
						if(distance == 10000){
							distance = -1;
							parts[1] = "";
						}
						String value = String.valueOf(distance) + "," + parts[1];
						return new Tuple2<String, String>(key, value);
						//return new Tuple2<String, String>(key, value);
					}
		});
		step5.saveAsTextFile(args[2]);
	}
}