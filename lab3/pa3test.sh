#/bin/bash
#  File:         pa1test
#  Author:       John Glick
#  Date:         October 26, 2015
#  Description:  bash shell script file for compiling and testing
#                programming project 1 of comp 370, fall 2015

#  Check for the correct number of arguments
EXPECTED_ARGS=1
if [ $# -ne $EXPECTED_ARGS ]; then
  echo Usage: pa1test filename
  exit
fi

#  Check that the file exists.
if [ ! -r ../$1 ]; then
  echo File $1 not found
  exit
fi

#  Iterate over all folders, each of which should have one file in it.
for dir in ../$1/*; do

    #  Message filename
  MESSFILE="$dir/testresults"
  
     # Get the program file
  FILETYPE="bad"
  for file in $dir/*; do
    if [[ $file == *.java ]]; then 
      PROGFILE=$file
      FILETYPE="java"
      break
    elif [[ $file == *.py ]]; then 
      PROGFILE=$file
      FILETYPE="python"
      break
    elif [[ $file == *.c ]]; then 
      PROGFILE=$file
      FILETYPE="c"
      break
    fi
  done

  if [ $FILETYPE == "bad" ]; then
    echo No valid program file > $MESSFILE
    continue
  fi

    # Get classname
  FILENAME=$(basename $PROGFILE)
  CLASSNAME=${FILENAME%.*}

  echo ""
  echo ""
  echo Directory $dir
  echo Program file is $PROGFILE
  echo Class name is $CLASSNAME

#  Copy file over
  cp $PROGFILE .

#  Compile file if necessary.
#  Try to compile the class file. 
  if [ $FILETYPE == "java" ]; then
    echo Compiling $FILENAME  > $MESSFILE
    echo " " >> $MESSFILE
#   javac -encoding ISO-8859-1 $FILENAME 2>> $MESSFILE
    javac $FILENAME 2>> $MESSFILE
    if [ $? -ne 0 ]; then
      echo " " >> $MESSFILE
      echo Program $FILENAME did not compile. >> $MESSFILE
      echo Program $FILENAME did not compile.
      continue
    else
      echo " " >> $MESSFILE
      echo Program $FILENAME compiled. >> $MESSFILE
      echo Program $FILENAME compiled. 
    fi
    echo " " >> $MESSFILE
  elif [ $FILETYPE == "c" ]; then
    echo Compiling $FILENAM > $MESSFILE
    echo " " >> $MESSFILE
    gcc $FILENAME >> $MESSFILE
    if [ $? -ne 0 ]; then
      echo " " >> $MESSFILE
      echo Program $FILENAME did not compile. >> $MESSFILE
      echo Program $FILENAME did not compile.
      continue
    else
      echo " " >> $MESSFILE
      echo Program $FILENAME compiled. >> $MESSFILE
      echo Program $FILENAME compiled.
    fi
    echo " " >> $MESSFILE
  fi


#  Run test cases.

  NUM_TESTS=20
  NUM_CORRECT=0
  #for i in {1..19}
  for ((i=1; i <= NUM_TESTS; i++)); do
  # Test case i

    #  Run program on test case.
    echo "**********************" >> $MESSFILE
    echo Testing dfa$i >> $MESSFILE
    if [ $FILETYPE == "java" ]; then
      gtimeout 5 java $CLASSNAME ../testcases/re${i}In.txt re${i}Out.txt 2>> $MESSFILE
      if [ $? -ne 0 ]; then
        echo "   " $CLASSNAME did not terminate normally >> $MESSFILE
        continue
      else
        echo "   " $CLASSNAME terminated normally. >> $MESSFILE
      fi
    elif [ $FILETYPE == "c" ]; then
      ./a.out ../testcases/re${i}In.txt re${i}Out.txt 2>> $MESSFILE
      if [ $? -ne 0 ]; then
        echo "   " $FILENAME did not terminate normally >> $MESSFILE
        continue
      else
        echo "   " $FILENAME terminated normally. >> $MESSFILE
      fi
    elif [ $FILETYPE == "python" ]; then
      python $FILENAME ../testcases/re${i}In.txt re${i}Out.txt 2>> $MESSFILE
      if [ $? -ne 0 ]; then
        echo "   " $FILENAME did not terminate normally >> $MESSFILE
        continue
      else
        echo "   " $FILENAME terminated normally. >> $MESSFILE
      fi
    fi

    #  Check that the output files exists.
    if [ ! -r re${i}Out.txt ]; then
      echo "   " File re${i}Out.txt not created >> $MESSFILE
    else
#     Check that simulation results are correct.
      diff -i -w re${i}Out.txt ../testcases/  >> $MESSFILE
      if [ $? -ne 0 ]; then
        echo "   " $CLASSNAME gave incorrect output for test input re${i}In.txt >> $MESSFILE
        echo "   " Differences between your output and correct output: >> $MESSFILE
        echo "   " Only different lines are shown. >> $MESSFILE
        echo "   " Lines from your output are preceded by a \<. >> $MESSFILE
        echo "   " Corresponding lines from the test output are preceded by a \>. >> $MESSFILE
      else
        echo "   " $CLASSNAME gave correct output for test input re${i}In.txt >> $MESSFILE
        NUM_CORRECT=$((NUM_CORRECT+1))
      fi
#     Remove the output file
      rm re${i}Out.txt
    fi
  done
  rm -f *.class
  rm -f *.java
  rm -f *.py
  echo "**********************" >> $MESSFILE
  echo "Number of tests = " $NUM_TESTS >> $MESSFILE
  echo "Number of tests = " $NUM_TESTS
  echo "Number correct = " $NUM_CORRECT >> $MESSFILE
  echo "Number correct = " $NUM_CORRECT
done
