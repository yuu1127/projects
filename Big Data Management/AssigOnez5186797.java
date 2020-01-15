import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import java.util.ArrayList;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.ArrayWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.Writable;
import org.apache.hadoop.io.WritableComparable;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

/*Documentation and code structure
My structure is use 2 mapper and 2 reducers for getting final result. Additionally, I made 2 custom writable and 1 custom writablecomparable and 1 customarraywritable.
For this assignment, input format is [user_id::movie_id::rating::timestamp] , and outputs must be [key:(movie_id1, movie_id2)  value: (user_id,rating1,rating2]] , so I noticed that firstly we need to make movie tuples for each user since outputs requires movie-rating pairs for each user.
Hence, what I did for first phrase is getting movie-rating values ( [moiveId1, rating1 movieID, rating2 …]) for each user using first mapper and reducer.
First mapper, it uses UserMovieWritable and just return [movie_id,rating] for each user.
Then, first reducer (MyReducer) aggregate them and output to temp file which display tuple ([movie1, rating1 movie2, rating2….])  for each user for each line.
After this process, we need to consider combination of movies therefore I made custom writablecomparable and second mapper receives the temp file as argument and returns tuples which movie pair (movieid1,movieid2) is key and user-ratings (user, rating1, rating2) is value.
I used two for loop since we need to compare all movies to make movie pairs (So if the number of movie is n , we need to compare for O(n2) times).
One note is for each user if it has only one movie tuple (the user watched only one movie) we can discard this tuple since we need to display movie pair for each user.
After making tuples for each movie pair, second Reducer do final job. For second reducer, we need to concatenate values for same key (movie pair) then compareTo function inside writablecomparable works to check keys pair.
Finally output value should be array so I used custom array writable and it puts values in array for each keys (key:(movie_id1, movie_id2) value: [(user_id1, rating1, rating2) (user_id2, rating1,rating2…..]).
 */


public class AssigOnez5186797 {


	// writable for first mapper making [key:user value: movieid,rating] for later mapper and reducer
	public static class UserMovieWritable implements Writable {

		private Text movie_id;
		private IntWritable rating;

		public UserMovieWritable() {
			this.movie_id = new Text("");
			this.rating = new IntWritable(-1);
		}

		public UserMovieWritable(Text movie_id,IntWritable rating) {
			super();
			this.movie_id = movie_id;
			this.rating = rating;
		}

		public Text getMovie_id() {
			return movie_id;
		}

		public void setMovie_id(Text movie_id) {
			this.movie_id = movie_id;
		}

		public IntWritable getRating() {
			return rating;
		}

		public void setRating(IntWritable rating) {
			this.rating = rating;
		}

		@Override
		public void readFields(DataInput data) throws IOException {
			this.movie_id.readFields(data);
			this.rating.readFields(data);
		}

		@Override
		public void write(DataOutput data) throws IOException {
			this.movie_id.write(data);
			this.rating.write(data);
		}

		public String toString() {
			return "(" + this.movie_id.toString() + "," + this.rating.toString() + ")";
		}
	}

	// WritableComparable for second mapper ,use comparable because key is (m1,m2) and we need to compare m1 and m2
	public static class M_combination implements WritableComparable<M_combination> {
		private Text movie_id1;
		private Text movie_id2;

		public M_combination() {
			this.movie_id1 = new Text("");
			this.movie_id2 = new Text("");
		}

		public M_combination(Text movie_id1,Text movie_id2) {
			super();
			this.movie_id1 = movie_id1;
			this.movie_id2 = movie_id2;
		}

		public Text get_m1() {
			return movie_id1;
		}

		public void set_m1(Text movie_id1) {
			this.movie_id1 = movie_id1;
		}

		public Text get_m2() {
			return movie_id2;
		}

		public void set_m2(Text movie_id2) {
			this.movie_id2 = movie_id2;
		}


		@Override
		public void readFields(DataInput data) throws IOException {
			// TODO Auto-generated method stub
			this.movie_id1.readFields(data);
			this.movie_id2.readFields(data);
		}

		@Override
		public void write(DataOutput data) throws IOException {
			// TODO Auto-generated method stub
			this.movie_id1.write(data);
			this.movie_id2.write(data);
		}


		@Override
		public int compareTo(M_combination c) {
			//return pValue.compareTo(cValue);
			int cmp = movie_id1.compareTo(c.movie_id1);
			if(cmp != 0) {
				return cmp;
			}
			cmp = movie_id2.compareTo(c.movie_id2);
			return cmp;

		}

		public String toString() {
			return "(" + this.movie_id1.toString() + "," + this.movie_id2.toString()+ ")";
		}

	}

	//make movie pair (M1,M2) [(U5,1,3)]

	//make other writable


	// writable for second mapper for value (userID,rating1,rating2)
	public static class User_ratings implements Writable {

		private Text user_id;
		private IntWritable rating1;
		private IntWritable rating2;

		public User_ratings() {
			this.user_id = new Text("");
			this.rating1 = new IntWritable(-1);
			this.rating2 = new IntWritable(-1);
		}

		public User_ratings(Text user_id,IntWritable rating1,IntWritable rating2) {
			super();
			this.user_id = user_id;
			this.rating1 = rating1;
			this.rating2 = rating2;
		}

		public Text get_User_id() {
			return user_id;
		}

		public void set_User_id(Text user_id) {
			this.user_id = user_id;
		}

		public IntWritable get_Rating1() {
			return rating1;
		}

		public void set_Rating1(IntWritable rating1) {
			this.rating1 = rating1;
		}

		public IntWritable get_Rating2() {
			return rating2;
		}

		public void set_Rating2(IntWritable rating2) {
			this.rating2 = rating2;
		}

		@Override
		public void readFields(DataInput data) throws IOException {
			this.user_id.readFields(data);
			this.rating1.readFields(data);
			this.rating2.readFields(data);
		}

		@Override
		public void write(DataOutput data) throws IOException {
			this.user_id.write(data);
			this.rating1.write(data);
			this.rating2.write(data);
		}

		public String toString() {
			return "(" + this.user_id.toString() + "," + this.rating1.toString() + "," + this.rating2.toString() + ")";
		}
	}

	// ArrayWritable for final output
	public static class MyArrayWritable extends ArrayWritable{
		public MyArrayWritable(Class<? extends Writable> valueClass, Writable[] values) {
			super(valueClass, values);
		}
		@Override
		public String toString() {
			String ret = null;
			for(Writable w: this.get())
				if(ret == null)
					ret = "[" + w.toString();
				else
					ret += "," + w.toString();
			return ret + "]";
		}
	}


	// first mapper [key:user value: movieid,rating]
	public static class FirstMapper extends Mapper<LongWritable, Text, Text, UserMovieWritable> {

		@Override
		protected void map(LongWritable key, Text value, Mapper<LongWritable, Text, Text, UserMovieWritable>.Context context)
				throws IOException, InterruptedException {
			//value.toString().split(",") split
			String [] parts = value.toString().split("::");
			UserMovieWritable val = new UserMovieWritable();
			//only need to get name
			val.setMovie_id(new Text(parts[1]));
			val.setRating(new IntWritable(Integer.parseInt(parts[2])));
			context.write(new Text(parts[0]),val);
		}
	}

	//Second  mapper [key:(movieid1,movieid2) value: (userid,rating1,rating2)]
	public static class SecondMapper extends Mapper<LongWritable, Text, M_combination, User_ratings> {

		@Override
		protected void map(LongWritable key, Text value, Mapper<LongWritable, Text, M_combination, User_ratings>.Context context)
				throws IOException, InterruptedException {
			//value.toString().split(",") split
			String [] parts = value.toString().split("	");
			String [] movies = parts[1].toString().split(" ");
//			System.out.println("aaaaaaaaaaaaaaaaaa");
			if(movies.length > 1) {
				//java for roop for iterater part1
				for(int i = 0;i < movies.length;i++) {
					String [] movie1 = movies[i].toString().split(",");
					for(int j = i + 1;j < movies.length;j++) {
						//String [] movie1 = movies[i].toString().split(",");
						String [] movie2 = movies[j].toString().split(",");

						M_combination keys = new M_combination();
						User_ratings val = new User_ratings();

						keys.set_m1(new Text(movie1[0]));
						keys.set_m2(new Text(movie2[0]));

						val.set_User_id(new Text(parts[0]));
						val.set_Rating1(new IntWritable(Integer.parseInt(movie1[1])));
						val.set_Rating2(new IntWritable(Integer.parseInt(movie2[1])));

						//need ass1 and ass2
						//System.out.print(keys.toString());
						//System.out.println(val.toString());
						context.write(keys, val);
					}
				}
			}
		}
	}

	//first reducer to output for each user movies list for each line
	public static class MyReducer extends Reducer<Text, UserMovieWritable, Text, Text> {


		@Override
		protected void reduce(Text key, Iterable<UserMovieWritable> values,
				Reducer<Text, UserMovieWritable, Text, Text>.Context context) throws IOException, InterruptedException {

			UserMovieWritable value = new UserMovieWritable();
			String s = "";

			for(UserMovieWritable a: values) {
				value.setMovie_id(new Text(a.getMovie_id().toString()));
				value.setRating(new IntWritable(a.getRating().get()));
				s += value.getMovie_id().toString() + "," + value.getRating().toString() + " ";
			}
			context.write(key, new Text(s));
		}

	}

	//<key,value,key,value>

	//second reducer remove userID who watch just 1 movie since this assignment need movie pair for each user
	//outputs must be array so change to array outputs
	public static class MyReducer2 extends Reducer<M_combination, User_ratings, M_combination, MyArrayWritable> {

		@Override
		protected void reduce(M_combination key, Iterable<User_ratings> values,
				Reducer<M_combination, User_ratings, M_combination, MyArrayWritable>.Context context)
				throws IOException, InterruptedException {
			// TODO Auto-generated method stub
			// System.out.println("bbbbbbbbbbbbbbb");
			ArrayList<User_ratings> vals = new ArrayList<User_ratings>();
			while(values.iterator().hasNext()) {

				User_ratings a = new User_ratings();
				a = values.iterator().next();
				vals.add(new User_ratings(new Text(a.get_User_id()),new IntWritable(a.get_Rating1().get()),new IntWritable(a.get_Rating2().get())));
			}
			// System.out.println(vals.size());
			Writable [] myarray = new User_ratings[vals.size()];
			for(int i = 0; i < vals.size();i++) {
				myarray[i] = vals.get(i);
			}
			MyArrayWritable val = new MyArrayWritable(User_ratings.class,myarray);
			context.write(key,val);
		}
	}

	// using chain job ,just indicate which is input in FileInputFormat for me made temp file to store halfway result
	public static void main(String[] args) throws Exception {

		Configuration conf = new Configuration();

		Job job = Job.getInstance(conf, "Assign Join1");

	    job.setMapperClass(FirstMapper.class);
	    job.setReducerClass(MyReducer.class);

		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(UserMovieWritable.class);

	    job.setOutputKeyClass(Text.class);
	    job.setOutputValueClass(UserMovieWritable.class);

	    job.setInputFormatClass(TextInputFormat.class);

	    FileInputFormat.addInputPath(job, new Path(args[0]));
	    FileOutputFormat.setOutputPath(job, new Path("Temp"));

	    job.waitForCompletion(true);

		Job job1 = Job.getInstance(conf, "Assign Join2");

	    job1.setMapperClass(SecondMapper.class);
	    job1.setReducerClass(MyReducer2.class);

		job1.setMapOutputKeyClass(M_combination.class);
		job1.setMapOutputValueClass(User_ratings.class);

	    job1.setOutputKeyClass(M_combination.class);
	    job1.setOutputValueClass(MyArrayWritable.class);

	    job1.setInputFormatClass(TextInputFormat.class);

	    FileInputFormat.addInputPath(job1, new Path("Temp/part-r-00000"));
	    FileOutputFormat.setOutputPath(job1, new Path(args[1]));

	    job1.waitForCompletion(true);
		//job1

	}

}